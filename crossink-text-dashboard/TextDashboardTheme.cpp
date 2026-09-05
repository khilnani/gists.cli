#include "TextDashboardTheme.h"

#include <GfxRenderer.h>
#include <I18n.h>

#include <algorithm>
#include <cstdio>
#include <string>

#include "RecentBooksStore.h"
#include "activities/reader/BookReadingStats.h"
#include "components/TouchRegistry.h"
#include "fontIds.h"

namespace {
constexpr int kSidePadding = 42;
constexpr int kTopPadding = 46;
constexpr int kSectionGap = 22;
constexpr int kTitleLineGap = 4;
constexpr int kProgressBarHeight = 10;
constexpr int kProgressBarTopGap = 12;
constexpr int kProgressLabelGap = 8;

int drawWrappedText(const GfxRenderer& renderer, const int fontId, const int x, int y, const int maxWidth,
                    const int maxLines, const char* text, const EpdFontFamily::Style style,
                    const int lineGap = 0) {
  if (text == nullptr || text[0] == '\0') return y;
  const auto lines = renderer.wrappedText(fontId, text, maxWidth, maxLines, style);
  const int lineHeight = renderer.getLineHeight(fontId);
  for (const auto& line : lines) {
    renderer.drawText(fontId, x, y, line.c_str(), true, style);
    y += lineHeight + lineGap;
  }
  return y;
}
}  // namespace

void TextDashboardTheme::drawRecentBookCover(GfxRenderer& renderer, Rect rect,
                                             const std::vector<RecentBook>& recentBooks, int selectorIndex,
                                             bool& coverRendered, bool& coverBufferStored, bool& bufferRestored,
                                             const std::function<bool()>& storeCoverBuffer,
                                             const BookReadingStats* stats, float progressPercent,
                                             const GlobalReadingStats* globalStats,
                                             const char* currentChapterTitle) const {
  (void)selectorIndex;
  (void)storeCoverBuffer;
  (void)globalStats;
  (void)currentChapterTitle;

  // There is deliberately no bitmap/cache path for this theme. HomeActivity
  // also suppresses its deferred thumbnail-generation pass while this theme is active.
  coverRendered = false;
  coverBufferStored = false;
  bufferRestored = false;

  const int contentX = rect.x + kSidePadding;
  const int contentWidth = std::max(1, rect.width - kSidePadding * 2);
  int y = rect.y + kTopPadding;

  if (recentBooks.empty()) {
    const char* emptyLabel = tr(STR_NO_OPEN_BOOK);
    const auto lines = renderer.wrappedText(LEXENDDECA_16_FONT_ID, emptyLabel, contentWidth, 2, EpdFontFamily::BOLD);
    const int lineHeight = renderer.getLineHeight(LEXENDDECA_16_FONT_ID);
    const int blockHeight = static_cast<int>(lines.size()) * lineHeight;
    int emptyY = rect.y + std::max(0, (rect.height - blockHeight) / 2);
    for (const auto& line : lines) {
      const int lineWidth = renderer.getTextWidth(LEXENDDECA_16_FONT_ID, line.c_str(), EpdFontFamily::BOLD);
      renderer.drawText(LEXENDDECA_16_FONT_ID, rect.x + (rect.width - lineWidth) / 2, emptyY, line.c_str(), true,
                        EpdFontFamily::BOLD);
      emptyY += lineHeight;
    }
    return;
  }

  const RecentBook& book = recentBooks.front();
  TouchRegistry::getInstance().add(rect, 0, TouchRegistry::Cover);

  renderer.drawText(UI_10_FONT_ID, contentX, y, tr(STR_CONTINUE_READING), true, EpdFontFamily::BOLD);
  y += renderer.getLineHeight(UI_10_FONT_ID) + kSectionGap;

  const std::string& title = book.title.empty() ? book.path : book.title;
  y = drawWrappedText(renderer, LEXENDDECA_16_FONT_ID, contentX, y, contentWidth, 4, title.c_str(),
                      EpdFontFamily::BOLD, kTitleLineGap);

  if (!book.author.empty()) {
    y += 8;
    y = drawWrappedText(renderer, UI_12_FONT_ID, contentX, y, contentWidth, 2, book.author.c_str(),
                        EpdFontFamily::REGULAR, 2);
  }

  y += kSectionGap;
  renderer.drawLine(contentX, y, contentX + contentWidth, y, true);
  y += kSectionGap;

  if (progressPercent >= 0.0f) {
    const int progress = std::clamp(static_cast<int>(progressPercent + 0.5f), 0, 100);
    char progressLabel[12];
    snprintf(progressLabel, sizeof(progressLabel), "%d%%", progress);
    renderer.drawText(LEXENDDECA_16_FONT_ID, contentX, y, progressLabel, true, EpdFontFamily::BOLD);
    y += renderer.getLineHeight(LEXENDDECA_16_FONT_ID) + kProgressBarTopGap;

    const int barWidth = contentWidth;
    renderer.drawRect(contentX, y, barWidth, kProgressBarHeight, true);
    const int innerWidth = std::max(0, barWidth - 2);
    const int fillWidth = (innerWidth * progress) / 100;
    if (fillWidth > 0) {
      renderer.fillRect(contentX + 1, y + 1, fillWidth, kProgressBarHeight - 2, true);
    }
    y += kProgressBarHeight + kProgressLabelGap;
  } else {
    renderer.drawText(UI_12_FONT_ID, contentX, y, tr(STR_START_READING));
    y += renderer.getLineHeight(UI_12_FONT_ID) + kSectionGap;
  }

  if (stats != nullptr && stats->totalReadingSeconds > 0) {
    char duration[32];
    BookReadingStats::formatDuration(stats->totalReadingSeconds, duration, sizeof(duration));
    const char* label = tr(STR_STATS_TOTAL_READING_TIME_LBL_SHORT);
    const int durationWidth = renderer.getTextWidth(UI_12_FONT_ID, duration, EpdFontFamily::BOLD);
    renderer.drawText(UI_12_FONT_ID, contentX, y, label);
    renderer.drawText(UI_12_FONT_ID, contentX + contentWidth - durationWidth, y, duration, true, EpdFontFamily::BOLD);
  }
}
