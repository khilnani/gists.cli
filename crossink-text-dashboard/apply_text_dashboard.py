#!/usr/bin/env python3
"""Apply the Text Dashboard theme to CrossInk v1.5.1-rc-6 source."""
from pathlib import Path
import sys

ROOT = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd()


def replace_once(path: str, old: str, new: str) -> None:
    p = ROOT / path
    text = p.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"Expected exactly one match in {path}, found {count}. Wrong CrossInk revision?")
    p.write_text(text.replace(old, new, 1), encoding="utf-8")


replace_once(
    "src/CrossPointSettings.h",
    """    MINIMAL = 5,\n    DASHBOARD = 6,\n    UI_THEME_COUNT = 7\n""",
    """    MINIMAL = 5,\n    DASHBOARD = 6,\n    TEXT_DASHBOARD = 7,\n    UI_THEME_COUNT = 8\n""",
)

replace_once(
    "lib/I18n/translations/english.yaml",
    'STR_THEME_MINIMAL: "Minimal"\nSTR_THEME_DASHBOARD: "Dashboard"\n',
    'STR_THEME_MINIMAL: "Minimal"\nSTR_THEME_TEXT_DASHBOARD: "Text Dashboard"\nSTR_THEME_DASHBOARD: "Dashboard"\n',
)

replace_once(
    "src/SettingsList.h",
    """            {StrId::STR_THEME_CLASSIC, StrId::STR_THEME_MINIMAL, StrId::STR_THEME_DASHBOARD, StrId::STR_THEME_LYRA,\n             StrId::STR_THEME_LYRA_EXTENDED, StrId::STR_THEME_LYRA_CAROUSEL, StrId::STR_THEME_ROUNDEDRAFF},\n            \"uiTheme\", StrId::STR_CAT_DISPLAY)\n            .withEnumRawValues({CrossPointSettings::UI_THEME::CLASSIC, CrossPointSettings::UI_THEME::MINIMAL,\n                                CrossPointSettings::UI_THEME::DASHBOARD, CrossPointSettings::UI_THEME::LYRA,\n                                CrossPointSettings::UI_THEME::LYRA_3_COVERS,\n                                CrossPointSettings::UI_THEME::LYRA_CAROUSEL,\n                                CrossPointSettings::UI_THEME::ROUNDEDRAFF}));\n""",
    """            {StrId::STR_THEME_CLASSIC, StrId::STR_THEME_MINIMAL, StrId::STR_THEME_TEXT_DASHBOARD,\n             StrId::STR_THEME_DASHBOARD, StrId::STR_THEME_LYRA, StrId::STR_THEME_LYRA_EXTENDED,\n             StrId::STR_THEME_LYRA_CAROUSEL, StrId::STR_THEME_ROUNDEDRAFF},\n            \"uiTheme\", StrId::STR_CAT_DISPLAY)\n            .withEnumRawValues({CrossPointSettings::UI_THEME::CLASSIC, CrossPointSettings::UI_THEME::MINIMAL,\n                                CrossPointSettings::UI_THEME::TEXT_DASHBOARD, CrossPointSettings::UI_THEME::DASHBOARD,\n                                CrossPointSettings::UI_THEME::LYRA, CrossPointSettings::UI_THEME::LYRA_3_COVERS,\n                                CrossPointSettings::UI_THEME::LYRA_CAROUSEL,\n                                CrossPointSettings::UI_THEME::ROUNDEDRAFF}));\n""",
)

replace_once(
    "src/components/UITheme.cpp",
    '#include "components/themes/minimal/MinimalTheme.h"\n#include "components/themes/roundedraff/RoundedRaffTheme.h"\n',
    '#include "components/themes/minimal/MinimalTheme.h"\n#include "components/themes/roundedraff/RoundedRaffTheme.h"\n#include "components/themes/textdashboard/TextDashboardTheme.h"\n',
)
replace_once(
    "src/components/UITheme.cpp",
    """    case CrossPointSettings::UI_THEME::DASHBOARD:\n      LOG_DBG(\"UI\", \"Using Dashboard theme\");\n      currentTheme = std::make_unique<DashboardTheme>();\n      currentMetrics = &DashboardMetrics::values;\n      break;\n""",
    """    case CrossPointSettings::UI_THEME::DASHBOARD:\n      LOG_DBG(\"UI\", \"Using Dashboard theme\");\n      currentTheme = std::make_unique<DashboardTheme>();\n      currentMetrics = &DashboardMetrics::values;\n      break;\n    case CrossPointSettings::UI_THEME::TEXT_DASHBOARD:\n      LOG_DBG(\"UI\", \"Using Text Dashboard theme\");\n      currentTheme = std::make_unique<TextDashboardTheme>();\n      currentMetrics = &MinimalMetrics::values;\n      break;\n""",
)

replace_once(
    "src/activities/home/HomeActivity.cpp",
    """bool isDashboardTheme() {\n  return static_cast<CrossPointSettings::UI_THEME>(SETTINGS.uiTheme) == CrossPointSettings::UI_THEME::DASHBOARD;\n}\n\nbool usesMinimalHomeInteraction() { return isMinimalTheme() || isDashboardTheme(); }\n""",
    """bool isDashboardTheme() {\n  return static_cast<CrossPointSettings::UI_THEME>(SETTINGS.uiTheme) == CrossPointSettings::UI_THEME::DASHBOARD;\n}\n\nbool isTextDashboardTheme() {\n  return static_cast<CrossPointSettings::UI_THEME>(SETTINGS.uiTheme) ==\n         CrossPointSettings::UI_THEME::TEXT_DASHBOARD;\n}\n\nbool usesMinimalHomeInteraction() { return isMinimalTheme() || isDashboardTheme() || isTextDashboardTheme(); }\n""",
)
replace_once(
    "src/activities/home/HomeActivity.cpp",
    """    ensureReusableCoverPath(book);\n    recentBooks.push_back(book);\n""",
    """    if (!isTextDashboardTheme()) {\n      ensureReusableCoverPath(book);\n    }\n    recentBooks.push_back(book);\n""",
)
replace_once(
    "src/activities/home/HomeActivity.cpp",
    """  RECENT_BOOKS.ensureLoaded();\n  loadRecentBooks(recentBooksToLoad);\n\n  const auto selectInitialBook = [this, &metrics](const std::string& path) {\n""",
    """  RECENT_BOOKS.ensureLoaded();\n  loadRecentBooks(recentBooksToLoad);\n\n  // Text Dashboard intentionally never touches cover thumbnails on Home.\n  // Mark the deferred cover pass complete so the second render remains text-only.\n  if (isTextDashboardTheme()) {\n    recentsLoaded = true;\n    recentsLoading = false;\n  }\n\n  const auto selectInitialBook = [this, &metrics](const std::string& path) {\n""",
)

theme_dir = ROOT / "src/components/themes/textdashboard"
theme_dir.mkdir(parents=True, exist_ok=True)
source_dir = Path(__file__).resolve().parent
for name in ("TextDashboardTheme.h", "TextDashboardTheme.cpp"):
    (theme_dir / name).write_text((source_dir / name).read_text(encoding="utf-8"), encoding="utf-8")

print("Text Dashboard applied.")
print("Build X3/X4 firmware with: pio run -e default")
