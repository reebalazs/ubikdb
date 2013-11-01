#! /bin/sh

# This should be .... python, to allow it to run in windows.
# ... properly integrated as a console script or in supervisor
# ... actually minify (uglify) and not just concat
# ... should autocompile anyway, if there are changes.
#
# For now, just run this to update the javascripts in substanced.

HERE=`dirname $0`
SLICKGRID=$HERE/../src/slickgrid
SUBSTANCED=$HERE/../src/substanced/substanced/sdi/static

# Remark about jquery-ui:
#
# We don't need the whole jquery-ui. We only need the helpers
# for column reorder and resize, and their dependencies.
# (And, even these helpers will need to be omitted,
# if once we add a different support for column handling.)

cat \
    $SLICKGRID/lib/jquery-ui-1.8.16/jquery.ui.core.js \
    $SLICKGRID/lib/jquery-ui-1.8.16/jquery.ui.widget.js \
    $SLICKGRID/lib/jquery-ui-1.8.16/jquery.ui.mouse.js \
    $SLICKGRID/lib/jquery-ui-1.8.16/jquery.ui.resizable.js \
    $SLICKGRID/lib/jquery-ui-1.8.16/jquery.ui.sortable.js \
    $SLICKGRID/lib/jquery.event.drag-2.0.min.js \
    $SLICKGRID/lib/jquery.event.drop-2.0.min.js \
    $SLICKGRID/slick.dataview.js \
    $SLICKGRID/slick.core.js \
    $SLICKGRID/slick.grid.js \
    $SLICKGRID/plugins/slick.rowselectionmodel.js \
    $SLICKGRID/plugins/slick.checkboxselectcolumn.js \
    $SLICKGRID/plugins/slick.rowmovemanager.js \
    $SLICKGRID/plugins/slick.responsiveness.js \
    $SLICKGRID/bootstrap/bootstrap-slickgrid.js \
    > $SUBSTANCED/js/slickgrid.upstream.js

    #$SLICKGRID/slick.editors.js \
    #$SLICKGRID/controls/slick.columnpicker.js \

    #$SLICKGRID/lib/jquery-ui-1.8.16.custom.min.js \

# We also need to copy the css files to substanced, because
# LESS's @import is a real import, consequently it will fail
# in runtime because the sources will be offline in runtime.
cat \
    $SLICKGRID/slick.grid.css \
    > $SUBSTANCED/css/slick.grid.upstream.css

    #$SLICKGRID/controls/slick.columnpicker.css \

