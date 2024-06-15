import re

from PySide6.QtCore import QObject, Signal


class SmartSignal(object):
    """
    Makes connections in PySide easier.
    """

    def _do_connection(self, wgt, sig, func):
        """
        Make a connection between a GUI widget and a callable.

        wgt and sig are strings with widget and signal name
        func is a callable for that signal
        """
        # new style  (we use this)
        # self.btn_name.clicked.connect(self.on_btn_name_clicked)
        # old style
        # self.connect(self.btn_name, SIGNAL('clicked()'), self.on_btn_name_clicked)

        if not hasattr(self, wgt):
            return False
        
        
        wgtobj = getattr(self, wgt)
        if not hasattr(wgtobj, sig):
            return False
        
        
        sigobj = getattr(wgtobj, sig)
        if not isinstance(sigobj, Signal):
            return False
        
        sigobj.connect(func)
        return True

    def _process_list(self, l):
        """
        Processes a list of widget names.

        If any name is between `` then it is supposed to be a regex.
        """
        if hasattr(self, l):
            t = getattr(self, l)

            def proc(inp: str):

                if inp.startswith("`"):
                    r = re.compile(inp.lstrip("`"))
                    return [
                        u
                        for u in [
                            m.group() for m in [r.match(x) for x in dir(self)] if m
                        ]
                        if isinstance(getattr(self, u), QObject)
                    ]
                else:
                    return [inp]

            return list(set([y for x in map(proc, t) for y in x]))

        return []

    def auto_connect(self):
        """
        Make a connection between every member function to a GUI signal.

        Every member function whose name is in format:

        '_on_' + <widget_name> + '__' + <widget_signal_name>

        are connected to the signal of a GUI widget if it exists.

        Also, every function with format:

        '_when_' + <group_name> + '__' + <widget_signal_name>

        should also define a string named: '_' + <group_name> on class level

        _group1 = 'btn_add, btn_remove, `btn_l.+`, btn_test'
        _when_group1__clicked(self):
            who = self.sender()
            #use who to discover who called this callback

        inside the string you can use regex surronded by `` to select related widgets
        """
        for o in dir(self):
            if o.endswith("_receiver") and "__" in o:
                func = getattr(self, o)
                wgt, sig = o.rstrip("_receiver").split("__")
                if not self._do_connection(wgt, sig, func):
                    print("Failed to connect", o)

            if o.endswith("_receivers") and "__" in o:
                func = getattr(self, o)
                lst, sig = o.rstrip("_receivers").split("__")
                lst = self._process_list(lst)  # 5 to keep _ at beggining
                for wgt in lst:
                    if not self._do_connection(wgt, sig, func):
                        print("Failed to connect", o)

    # def print_signals_and_slots(self):
    #     """
    #     List all active Slots and Signal.

    #     Credits to: http://visitusers.org/index.php?title=PySide_Recipes#Debugging
    #     """
    #     for i in range(self.metaObject().methodCount()):
    #          m = self.metaObject().method(i)
    #          if m.methodType() == QMetaMethod.MethodType.Signal:
    #              print("SIGNAL: sig=", m.signature(), "hooked to nslots=", self.receivers(SIGNAL(m.signature())))
    #          elif m.methodType() == QMetaMethod.MethodType.Slot:
    #              print("SLOT: sig=", m.signature())

    def print_all_signals(self):
        """
        Prints out every signal available for this widget and childs.
        """
        for o in dir(self):
            obj = getattr(self, o)
            # print o, type(obj)
            div = False
            for c in dir(obj):
                cobj = getattr(obj, c)
                if isinstance(cobj, Signal):
                    print("def _on_{}__{}(self):".format(o, c))
                    div = True

            if div:
                print("-" * 30)
