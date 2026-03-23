import gi
import builtins


def _py2_unicode(obj=b"", encoding="utf-8", errors="strict"):
    if isinstance(obj, bytes):
        return obj.decode(encoding, errors)
    if isinstance(obj, str):
        return obj
    return str(obj)


if not hasattr(builtins, "unicode"):
    builtins.unicode = _py2_unicode
if not hasattr(builtins, "xrange"):
    builtins.xrange = range
if not hasattr(builtins, "long"):
    builtins.long = int
if not hasattr(builtins, "basestring"):
    builtins.basestring = (str, bytes)


gi.require_version('Gtk', '3.0')
gi.require_version('PangoCairo', '1.0')
try:
    gi.require_version('GtkSource', '4')
except ValueError:
    try:
        gi.require_version('GtkSource', '3.0')
    except ValueError:
        pass

from gi.repository import Gtk, Gdk, GObject, Pango, PangoCairo, GLib
try:
    from gi.repository import GtkSource
except Exception:
    GtkSource = None



# Old PyGTK signal compatibility for expose_event on Gtk.DrawingArea / widgets.
_GObject_connect = GObject.Object.connect


def _compat_connect(self, detailed_signal, handler, *args):
    if detailed_signal == 'expose_event':
        def _draw_wrapper(widget, cr, *extra):
            # Provide old-style convenience attributes used by PyGTK-era code.
            try:
                widget.window = widget.get_window()
            except Exception:
                pass
            try:
                alloc = widget.get_allocation()
                widget.allocation = (alloc.x, alloc.y, alloc.width, alloc.height)
            except Exception:
                pass
            class _CompatEvent:
                pass
            event = _CompatEvent()
            try:
                event.window = widget.get_window()
            except Exception:
                event.window = None
            return handler(widget, event, *args)
        return _GObject_connect(self, 'draw', _draw_wrapper)
    return _GObject_connect(self, detailed_signal, handler, *args)


GObject.Object.connect = _compat_connect

# Old PyGTK property-style accessors used throughout the codebase.
try:
    Gtk.Widget.window = property(lambda self: self.get_window())
except Exception:
    pass
def _compat_allocation(self):
    alloc = self.get_allocation()
    return (alloc.x, alloc.y, alloc.width, alloc.height)

try:
    Gtk.Widget.allocation = property(_compat_allocation)
except Exception:
    pass


def _set_data(self, key, value):
    store = getattr(self, '_pygtk_data_store', None)
    if store is None:
        store = {}
        setattr(self, '_pygtk_data_store', store)
    store[key] = value


def _get_data(self, key):
    store = getattr(self, '_pygtk_data_store', None)
    if store is None:
        return None
    return store.get(key)

Gtk.Widget.set_data = _set_data
Gtk.Widget.get_data = _get_data

# Export pygtk-like names.
gtk = Gtk
gdk = Gdk
gobject = GObject
pango = Pango
pangocairo = PangoCairo
gtksourceview2 = GtkSource

for name, value in {
    'WINDOW_TOPLEVEL': Gtk.WindowType.TOPLEVEL,
    'POS_BOTTOM': Gtk.PositionType.BOTTOM,
    'POLICY_AUTOMATIC': Gtk.PolicyType.AUTOMATIC,
    'EXPAND': Gtk.AttachOptions.EXPAND,
    'FILL': Gtk.AttachOptions.FILL,
    'RELIEF_NONE': Gtk.ReliefStyle.NONE,
    'ICON_SIZE_MENU': Gtk.IconSize.MENU,
    'FILE_CHOOSER_ACTION_SAVE': Gtk.FileChooserAction.SAVE,
    'FILE_CHOOSER_ACTION_OPEN': Gtk.FileChooserAction.OPEN,
    'RESPONSE_OK': Gtk.ResponseType.OK,
    'RESPONSE_CANCEL': Gtk.ResponseType.CANCEL,
    'ACCEL_VISIBLE': Gtk.AccelFlags.VISIBLE,
    'TARGET_SAME_APP': Gtk.TargetFlags.SAME_APP,
    'TREE_VIEW_GRID_LINES_HORIZONTAL': Gtk.TreeViewGridLines.HORIZONTAL,
    'STOCK_OK': 'gtk-ok',
    'STOCK_CANCEL': 'gtk-cancel',
    'STOCK_OPEN': 'gtk-open',
    'STOCK_CLOSE': 'gtk-close',
    'STOCK_NEW': 'gtk-new',
    'STOCK_SAVE': 'gtk-save',
    'STOCK_QUIT': 'gtk-quit',
    'STOCK_HELP': 'gtk-help',
}.items():
    setattr(gtk, name, value)

setattr(gtk, 'gdk', gdk)
setattr(gdk, 'BUTTON1_MASK', Gdk.ModifierType.BUTTON1_MASK)
setattr(gdk, 'BUTTON_PRESS_MASK', Gdk.EventMask.BUTTON_PRESS_MASK)
setattr(gdk, 'BUTTON_RELEASE_MASK', Gdk.EventMask.BUTTON_RELEASE_MASK)
setattr(gdk, 'POINTER_MOTION_MASK', Gdk.EventMask.POINTER_MOTION_MASK)
setattr(gdk, 'SCROLL_MASK', Gdk.EventMask.SCROLL_MASK)
setattr(gdk, 'ACTION_DEFAULT', Gdk.DragAction.DEFAULT)
setattr(gdk, 'ACTION_COPY', Gdk.DragAction.COPY)
setattr(gdk, 'ACTION_MOVE', Gdk.DragAction.MOVE)
setattr(gdk, 'ACTION_LINK', Gdk.DragAction.LINK)
setattr(gdk, 'ACTION_PRIVATE', Gdk.DragAction.PRIVATE)
setattr(gdk, 'CONTROL_MASK', Gdk.ModifierType.CONTROL_MASK)
setattr(gdk, 'SHIFT_MASK', Gdk.ModifierType.SHIFT_MASK)
setattr(gdk, 'BUTTON_PRESS', Gdk.EventType.BUTTON_PRESS)
setattr(gdk, 'BUTTON_RELEASE', Gdk.EventType.BUTTON_RELEASE)
setattr(gdk, 'KEY_PRESS', Gdk.EventType.KEY_PRESS)
setattr(gdk, 'KEY_RELEASE', Gdk.EventType.KEY_RELEASE)
setattr(gdk, '_2BUTTON_PRESS', Gdk.EventType.DOUBLE_BUTTON_PRESS)
setattr(gdk, 'SCROLL_UP', Gdk.ScrollDirection.UP)
setattr(gdk, 'SCROLL_DOWN', Gdk.ScrollDirection.DOWN)
setattr(gdk, 'SCROLL_LEFT', Gdk.ScrollDirection.LEFT)
setattr(gdk, 'SCROLL_RIGHT', Gdk.ScrollDirection.RIGHT)

setattr(gobject, 'TYPE_STRING', GObject.TYPE_STRING)
setattr(gobject, 'TYPE_INT', GObject.TYPE_INT)
setattr(gobject, 'TYPE_NONE', GObject.TYPE_NONE)
setattr(gobject, 'SIGNAL_RUN_FIRST', GObject.SignalFlags.RUN_FIRST)
setattr(gobject, 'GError', GLib.GError)

class Tooltips:
    def set_tip(self, widget, text):
        widget.set_tooltip_text(text)

def recent_manager_get_default():
    return Gtk.RecentManager.get_default()

setattr(gtk, 'Tooltips', Tooltips)
setattr(gtk, 'recent_manager_get_default', recent_manager_get_default)

class Table(Gtk.Grid):
    def __init__(self, rows=1, columns=1, homogeneous=False):
        super().__init__()
        self.set_row_homogeneous(homogeneous)
        self.set_column_homogeneous(homogeneous)

    def attach(self, child, left_attach, right_attach, top_attach, bottom_attach, xoptions=None, yoptions=None, xpadding=0, ypadding=0):
        width = max(1, right_attach - left_attach)
        height = max(1, bottom_attach - top_attach)
        if xoptions is None:
            xexpand = True
            xfill = True
        else:
            xexpand = bool(xoptions & Gtk.AttachOptions.EXPAND) if isinstance(xoptions, int) else bool(xoptions)
            xfill = bool(xoptions & Gtk.AttachOptions.FILL) if isinstance(xoptions, int) else bool(xoptions)
        if yoptions is None:
            yexpand = True
            yfill = True
        else:
            yexpand = bool(yoptions & Gtk.AttachOptions.EXPAND) if isinstance(yoptions, int) else bool(yoptions)
            yfill = bool(yoptions & Gtk.AttachOptions.FILL) if isinstance(yoptions, int) else bool(yoptions)
        child.set_hexpand(xexpand)
        child.set_vexpand(yexpand)
        child.set_halign(Gtk.Align.FILL if xfill else Gtk.Align.START)
        child.set_valign(Gtk.Align.FILL if yfill else Gtk.Align.START)
        child.set_margin_start(xpadding)
        child.set_margin_end(xpadding)
        child.set_margin_top(ypadding)
        child.set_margin_bottom(ypadding)
        super().attach(child, left_attach, top_attach, width, height)

setattr(gtk, 'Table', Table)

class HBox(Gtk.Box):
    def __init__(self, homogeneous=False, spacing=0):
        super().__init__(orientation=Gtk.Orientation.HORIZONTAL, spacing=spacing)
        self.set_homogeneous(homogeneous)

class VBox(Gtk.Box):
    def __init__(self, homogeneous=False, spacing=0):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=spacing)
        self.set_homogeneous(homogeneous)

setattr(gtk, 'HBox', HBox)
setattr(gtk, 'VBox', VBox)


# Old PyGTK-style packing helpers with default arguments.
Gtk.Box._orig_pack_start = Gtk.Box.pack_start
Gtk.Box._orig_pack_end = Gtk.Box.pack_end


def _box_pack_start(self, child, expand=True, fill=True, padding=0):
    if padding:
        child.set_margin_start(max(child.get_margin_start(), padding))
        child.set_margin_end(max(child.get_margin_end(), padding))
        child.set_margin_top(max(child.get_margin_top(), padding))
        child.set_margin_bottom(max(child.get_margin_bottom(), padding))
    Gtk.Box._orig_pack_start(self, child, bool(expand), bool(fill), int(padding))


def _box_pack_end(self, child, expand=True, fill=True, padding=0):
    if padding:
        child.set_margin_start(max(child.get_margin_start(), padding))
        child.set_margin_end(max(child.get_margin_end(), padding))
        child.set_margin_top(max(child.get_margin_top(), padding))
        child.set_margin_bottom(max(child.get_margin_bottom(), padding))
    Gtk.Box._orig_pack_end(self, child, bool(expand), bool(fill), int(padding))


Gtk.Box.pack_start_defaults = _box_pack_start
Gtk.Box.pack_end_defaults = _box_pack_end


def _compat_pack_start(self, child, *args):
    if len(args) == 0:
        return _box_pack_start(self, child, True, True, 0)
    if len(args) == 1:
        return _box_pack_start(self, child, args[0], True, 0)
    if len(args) == 2:
        return _box_pack_start(self, child, args[0], args[1], 0)
    return _box_pack_start(self, child, *args[:3])


def _compat_pack_end(self, child, *args):
    if len(args) == 0:
        return _box_pack_end(self, child, True, True, 0)
    if len(args) == 1:
        return _box_pack_end(self, child, args[0], True, 0)
    if len(args) == 2:
        return _box_pack_end(self, child, args[0], args[1], 0)
    return _box_pack_end(self, child, *args[:3])


Gtk.Box.pack_start = _compat_pack_start
Gtk.Box.pack_end = _compat_pack_end


class Button(Gtk.Button):
    def __init__(self, label=None, *args, **kwargs):
        if label is not None and 'label' not in kwargs:
            kwargs['label'] = label
        super().__init__(*args, **kwargs)


class CheckButton(Gtk.CheckButton):
    def __init__(self, label=None, *args, **kwargs):
        if label is not None and 'label' not in kwargs:
            kwargs['label'] = label
        super().__init__(*args, **kwargs)


class Frame(Gtk.Frame):
    def __init__(self, label=None, *args, **kwargs):
        if label is not None and 'label' not in kwargs:
            kwargs['label'] = label
        super().__init__(*args, **kwargs)


setattr(gtk, 'Button', Button)
setattr(gtk, 'CheckButton', CheckButton)
setattr(gtk, 'Frame', Frame)


# Additional old gdk compatibility constants/helpers
setattr(gdk, 'BUTTON_PRESS_MASK', Gdk.EventMask.BUTTON_PRESS_MASK)
setattr(gdk, 'BUTTON_RELEASE_MASK', Gdk.EventMask.BUTTON_RELEASE_MASK)
setattr(gdk, 'POINTER_MOTION_MASK', Gdk.EventMask.POINTER_MOTION_MASK)
setattr(gdk, 'SHIFT_MASK', Gdk.ModifierType.SHIFT_MASK)
setattr(gdk, 'MOD1_MASK', Gdk.ModifierType.MOD1_MASK)
setattr(gdk, 'SELECTION_CLIPBOARD', Gdk.SELECTION_CLIPBOARD)

class _CompatColor:
    def __init__(self, red=0, green=0, blue=0):
        self.red = red
        self.green = green
        self.blue = blue

    def to_rgba(self):
        rgba = Gdk.RGBA()
        rgba.red = max(0.0, min(1.0, float(self.red) / 65535.0))
        rgba.green = max(0.0, min(1.0, float(self.green) / 65535.0))
        rgba.blue = max(0.0, min(1.0, float(self.blue) / 65535.0))
        rgba.alpha = 1.0
        return rgba

setattr(gdk, 'Color', _CompatColor)

# clipboard_get compatibility
def clipboard_get(selection=None):
    display = Gdk.Display.get_default()
    if selection is None:
        selection = Gdk.SELECTION_CLIPBOARD
    return Gtk.Clipboard.get_for_display(display, selection)

setattr(gtk, 'clipboard_get', clipboard_get)

# ColorButton compatibility for old Gdk.Color constructor usage
_OrigColorButton = Gtk.ColorButton
class ColorButton(_OrigColorButton):
    def __init__(self, color=None):
        if hasattr(color, 'to_rgba'):
            super().__init__(rgba=color.to_rgba())
        else:
            super().__init__()

setattr(gtk, 'ColorButton', ColorButton)


class FileChooserDialog(Gtk.FileChooserDialog):
    def __init__(self, title=None, parent=None, action=Gtk.FileChooserAction.OPEN, buttons=None):
        super().__init__(title=title, transient_for=parent, action=action)
        if buttons:
            self.add_buttons(*buttons)

setattr(gtk, 'FileChooserDialog', FileChooserDialog)


# ComboBoxEntry compatibility from old PyGTK.
if not hasattr(Gtk.ComboBox, "set_text_column") and hasattr(Gtk.ComboBox, "set_entry_text_column"):
    Gtk.ComboBox.set_text_column = Gtk.ComboBox.set_entry_text_column

def ComboBoxEntry(*args, **kwargs):
    try:
        cb = Gtk.ComboBox.new_with_entry()
    except Exception:
        cb = Gtk.ComboBox(has_entry=True)
    try:
        cb.child = cb.get_child()
    except Exception:
        pass
    return cb

setattr(gtk, 'ComboBoxEntry', ComboBoxEntry)


class VScrollbar(Gtk.Scrollbar):
    def __init__(self, adjustment=None):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, adjustment=adjustment)
        if adjustment is not None:
            self.set_adjustment(adjustment)

class HScrollbar(Gtk.Scrollbar):
    def __init__(self, adjustment=None):
        super().__init__(orientation=Gtk.Orientation.HORIZONTAL, adjustment=adjustment)
        if adjustment is not None:
            self.set_adjustment(adjustment)

setattr(gtk, 'VScrollbar', VScrollbar)
setattr(gtk, 'HScrollbar', HScrollbar)


# AccelGroup compatibility for old PyGTK connect_group API
def _accelgroup_connect_group(self, accel_key, accel_mods, accel_flags, callback):
    try:
        return self.connect(accel_key, accel_mods, accel_flags, callback)
    except TypeError:
        return None

Gtk.AccelGroup.connect_group = _accelgroup_connect_group
