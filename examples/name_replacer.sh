#!/bin/bash
# find_and_replace.sh

find . -type f -name "*.lp" -exec sed -i '' -e "s/backgroundcolor/background_color/g" {} +
find . -type f -name "*.lp" -exec sed -i '' -e "s/foregroundcolor/foreground_color/g" {} +

find . -type f -name "*.lp" -exec sed -i '' -e "s/onhover/on_hover/g" {} +
find . -type f -name "*.lp" -exec sed -i '' -e "s/hoverfore/hover_fore/g" {} +
find . -type f -name "*.lp" -exec sed -i '' -e "s/hoverback/hover_back/g" {} +
find . -type f -name "*.lp" -exec sed -i '' -e "s/hoverborder/hover_border/g" {} +

find . -type f -name "*.lp" -exec sed -i '' -e "s/fontfamily/font_family/g" {} +
find . -type f -name "*.lp" -exec sed -i '' -e "s/fontsize/font_size/g" {} +
find . -type f -name "*.lp" -exec sed -i '' -e "s/fontweight/font_weight/g" {} +

find . -type f -name "*.lp" -exec sed -i '' -e "s/resizablex/resizable_x/g" {} +
find . -type f -name "*.lp" -exec sed -i '' -e "s/resizabley/resizable_y/g" {} +

find . -type f -name "*.lp" -exec sed -i '' -e "s/childorg/child_layout/g" {} +
find . -type f -name "*.lp" -exec sed -i '' -e "s/gridcolumn/grid_column/g" {} +
find . -type f -name "*.lp" -exec sed -i '' -e "s/gridrow/grid_row/g" {} +
find . -type f -name "*.lp" -exec sed -i '' -e "s/rowspan/row_span/g" {} +
find . -type f -name "*.lp" -exec sed -i '' -e "s/columnspan/column_span/g" {} +

find . -type f -name "*.lp" -exec sed -i '' -e "s/posx/pos_x/g" {} +
find . -type f -name "*.lp" -exec sed -i '' -e "s/posy/pos_y/g" {} +

find . -type f -name "*.lp" -exec sed -i '' -e "s/borderwidth/border_width/g" {} +
find . -type f -name "*.lp" -exec sed -i '' -e "s/bordercolor/border_color/g" {} +


find . -type f -name "*.lp" -exec sed -i '' -e "s/dropdownmenu/dropdown_menu/g" {} +
find . -type f -name "*.lp" -exec sed -i '' -e "s/menuitem/menu_item/g" {} +
find . -type f -name "*.lp" -exec sed -i '' -e "s/menubar/menu_bar/g" {} +
find . -type f -name "*.lp" -exec sed -i '' -e "s/barsection/bar_section/g" {} +
find . -type f -name "*.lp" -exec sed -i '' -e "s/sectionitem/section_item/g" {} +





