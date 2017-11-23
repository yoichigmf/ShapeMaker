# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ShapeMaker
                                 A QGIS plugin
 林相境界 レイヤの作成
                              -------------------
        begin                : 2017-11-21
        git sha              : $Format:%H$
        copyright            : (C) 2017 by Yoichi Kayama
        email                : yoichi.kayama@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

from qgis.core import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.gui import QgsMessageBar

#from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
#from PyQt4.QtGui import QAction, QIcon, QFileDialog
# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
from ShapeMaker_dialog import ShapeMakerDialog
import os.path
#import QtGui

class ShapeMaker:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'ShapeMaker_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)


        # Declare instance attributes
        self.actions = []
        self.menu = u'林相境界作成'
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'林相境界作成')
        self.toolbar.setObjectName(u'ShapeMaker')

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('ShapeMaker', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        # Create the dialog (after translation) and keep reference
        self.dlg = ShapeMakerDialog()

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/ShapeMaker/icon.png'
        self.add_action(
            icon_path,
            text=u'林相境界作成',
            callback=self.run,
            parent=self.iface.mainWindow())
            
        self.dlg.pushButton.clicked.connect(self.browsefile)
        self.dlg.pushButton_2.clicked.connect(self.makelayer)
        self.dlg.pushButton_3.clicked.connect(self.closedlg )    
        
    def closedlg(self):
        self.dlg.reject()  
        
    def browsefile(self):
        shpfname  = QFileDialog.getSaveFileName(None,u'林相境界保存ファイル指定', None, u'shp(*.shp)' )
        
        self.dlg.plainTextEdit.setPlainText( shpfname )
        
    def makelayer(self):
        # create layer
           
        #  入力ファイル名のチェック
        if not self.dlg.plainTextEdit.find(u'.shp' ):
               self.iface.messageBar().pushMessage("Error", u'ファイル名が不正です (.shp) で終了するファイル名を指定して下さい', level=QgsMessageBar.CRITICAL)
               return           
           
        shpfname = self.dlg.plainTextEdit.toPlainText() 
        

        #  フィールド定義
        
        fields = QgsFields()
        
        fields.append(QgsField("ID", QVariant.Int))
        
        fields.append(QgsField(u'樹種',  QVariant.Int))    
        fields.append(QgsField(u'林齢',  QVariant.Int))
        fields.append(QgsField(u'樹高', QVariant.Double,'double', 4,2))
        fields.append(QgsField(u'胸高直径', QVariant.Double,'double', 4,2))
        fields.append(QgsField(u'本数密度', QVariant.Double,'double', 5,1))
        
        
        #  システムcrs 取得
        canvas = self.iface.mapCanvas()
        mapRenderer = canvas.mapRenderer()
        pcrs =mapRenderer.destinationCrs()
        
        writer = QgsVectorFileWriter( shpfname, "shift_jis", fields,QGis.WKBMultiPolygon, pcrs, "ESRI Shapefile" )
        
           
        #  書き込みエラーチェック
        if writer.hasError() != QgsVectorFileWriter.NoError:
               self.iface.messageBar().pushMessage("Error", writer.errorMessage(), level=QgsMessageBar.CRITICAL)
               #print("Error when creating shapefile: ", writer.errorMessage())
               del writer
               return
               
        del writer
 
        #  再度読み込み　       
        vl =  QgsVectorLayer(shpfname, u'林相', "ogr")
        vl.setProviderEncoding(u'shift_jis')
        
        layer_registry = QgsMapLayerRegistry.instance()
        layer_registry.addMapLayer(vl)
        self.dlg.reject()  



    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&ShapeMaker'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar


    def run(self):
        """Run method that performs all the real work"""
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass
