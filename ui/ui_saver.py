# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'saverZjYuyH.ui'
##
## Created by: Qt User Interface Compiler version 6.2.4
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################
try:
    from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
        QMetaObject, QObject, QPoint, QRect,
        QSize, QTime, QUrl, Qt)
    from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
        QFont, QFontDatabase, QGradient, QIcon,
        QImage, QKeySequence, QLinearGradient, QPainter,
        QPalette, QPixmap, QRadialGradient, QTransform)
    from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFrame,
        QGridLayout, QHBoxLayout, QHeaderView, QLabel,
        QLineEdit, QPushButton, QSizePolicy, QSpacerItem,
        QSpinBox, QStackedWidget, QTabWidget, QTableWidget,
        QTableWidgetItem, QTreeWidget, QTreeWidgetItem, QVBoxLayout,
        QWidget)

except:
    from PySide2.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
        QMetaObject, QObject, QPoint, QRect,
        QSize, QTime, QUrl, Qt)
    from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
        QFont, QFontDatabase, QGradient, QIcon,
        QImage, QKeySequence, QLinearGradient, QPainter,
        QPalette, QPixmap, QRadialGradient, QTransform)
    from PySide2.QtWidgets import (QApplication, QCheckBox, QComboBox, QFrame,
        QGridLayout, QHBoxLayout, QHeaderView, QLabel,
        QLineEdit, QPushButton, QSizePolicy, QSpacerItem,
        QSpinBox, QStackedWidget, QTabWidget, QTableWidget,
        QTableWidgetItem, QTreeWidget, QTreeWidgetItem, QVBoxLayout,
        QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(944, 798)
        self.horizontalLayout_2 = QHBoxLayout(Form)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.stackedWidget = QStackedWidget(Form)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.verticalLayout_11 = QVBoxLayout(self.page)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, -1, 0, 0)
        self.label_icon = QLabel(self.page)
        self.label_icon.setObjectName(u"label_icon")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_icon.sizePolicy().hasHeightForWidth())
        self.label_icon.setSizePolicy(sizePolicy)
        self.label_icon.setMaximumSize(QSize(40, 40))

        self.horizontalLayout.addWidget(self.label_icon)

        self.label = QLabel(self.page)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(22)
        font.setBold(True)
        self.label.setFont(font)

        self.horizontalLayout.addWidget(self.label, 0, Qt.AlignLeft)

        self.horizontalSpacer_11 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_11)

        self.label_user_name = QLabel(self.page)
        self.label_user_name.setObjectName(u"label_user_name")
        self.label_user_name.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout.addWidget(self.label_user_name)

        self.label_user_icon = QLabel(self.page)
        self.label_user_icon.setObjectName(u"label_user_icon")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_user_icon.sizePolicy().hasHeightForWidth())
        self.label_user_icon.setSizePolicy(sizePolicy1)
        self.label_user_icon.setMaximumSize(QSize(40, 40))

        self.horizontalLayout.addWidget(self.label_user_icon)


        self.verticalLayout_11.addLayout(self.horizontalLayout)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(-1, -1, -1, 0)
        self.tabWidget_file_list = QTabWidget(self.page)
        self.tabWidget_file_list.setObjectName(u"tabWidget_file_list")
        sizePolicy1.setHeightForWidth(self.tabWidget_file_list.sizePolicy().hasHeightForWidth())
        self.tabWidget_file_list.setSizePolicy(sizePolicy1)
        self.tabWidget_file_list.setMinimumSize(QSize(0, 400))
        self.tabWidget_file_list.setMaximumSize(QSize(16777215, 16777215))
        self.tab_4 = QWidget()
        self.tab_4.setObjectName(u"tab_4")
        self.verticalLayout_2 = QVBoxLayout(self.tab_4)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_2)

        self.lineEdit_search_all = QLineEdit(self.tab_4)
        self.lineEdit_search_all.setObjectName(u"lineEdit_search_all")
        self.lineEdit_search_all.setMaximumSize(QSize(200, 16777215))

        self.horizontalLayout_7.addWidget(self.lineEdit_search_all)


        self.verticalLayout_2.addLayout(self.horizontalLayout_7)

        self.treeWidget_grid_total = QTreeWidget(self.tab_4)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"1");
        self.treeWidget_grid_total.setHeaderItem(__qtreewidgetitem)
        self.treeWidget_grid_total.setObjectName(u"treeWidget_grid_total")
        self.treeWidget_grid_total.setMinimumSize(QSize(0, 380))
        self.treeWidget_grid_total.setMaximumSize(QSize(16777215, 16777215))
        self.treeWidget_grid_total.header().setVisible(False)

        self.verticalLayout_2.addWidget(self.treeWidget_grid_total)

        self.tabWidget_file_list.addTab(self.tab_4, "")
        self.tab_5 = QWidget()
        self.tab_5.setObjectName(u"tab_5")
        self.verticalLayout_5 = QVBoxLayout(self.tab_5)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.horizontalLayout_17 = QHBoxLayout()
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_17.addItem(self.horizontalSpacer_8)

        self.lineEdit_search_wip = QLineEdit(self.tab_5)
        self.lineEdit_search_wip.setObjectName(u"lineEdit_search_wip")
        self.lineEdit_search_wip.setMaximumSize(QSize(200, 16777215))

        self.horizontalLayout_17.addWidget(self.lineEdit_search_wip)


        self.verticalLayout_5.addLayout(self.horizontalLayout_17)

        self.tableWidget_list_wip = QTableWidget(self.tab_5)
        self.tableWidget_list_wip.setObjectName(u"tableWidget_list_wip")
        self.tableWidget_list_wip.setMinimumSize(QSize(0, 380))
        self.tableWidget_list_wip.setMaximumSize(QSize(16777215, 16777215))
        self.tableWidget_list_wip.horizontalHeader().setVisible(False)
        self.tableWidget_list_wip.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_list_wip.verticalHeader().setVisible(False)

        self.verticalLayout_5.addWidget(self.tableWidget_list_wip)

        self.tabWidget_file_list.addTab(self.tab_5, "")
        self.tab_6 = QWidget()
        self.tab_6.setObjectName(u"tab_6")
        self.verticalLayout_9 = QVBoxLayout(self.tab_6)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.horizontalLayout_18 = QHBoxLayout()
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_18.addItem(self.horizontalSpacer_9)

        self.lineEdit_search_pub = QLineEdit(self.tab_6)
        self.lineEdit_search_pub.setObjectName(u"lineEdit_search_pub")
        self.lineEdit_search_pub.setMaximumSize(QSize(200, 16777215))

        self.horizontalLayout_18.addWidget(self.lineEdit_search_pub)


        self.verticalLayout_9.addLayout(self.horizontalLayout_18)

        self.tableWidget_list_pub = QTableWidget(self.tab_6)
        self.tableWidget_list_pub.setObjectName(u"tableWidget_list_pub")
        self.tableWidget_list_pub.setMinimumSize(QSize(0, 380))
        self.tableWidget_list_pub.setMaximumSize(QSize(16777215, 16777215))
        self.tableWidget_list_pub.horizontalHeader().setVisible(False)
        self.tableWidget_list_pub.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_list_pub.verticalHeader().setVisible(False)
        self.tableWidget_list_pub.verticalHeader().setStretchLastSection(False)

        self.verticalLayout_9.addWidget(self.tableWidget_list_pub)

        self.tabWidget_file_list.addTab(self.tab_6, "")

        self.gridLayout_2.addWidget(self.tabWidget_file_list, 1, 1, 1, 1)

        self.label_project_name = QLabel(self.page)
        self.label_project_name.setObjectName(u"label_project_name")
        font1 = QFont()
        font1.setBold(True)
        self.label_project_name.setFont(font1)
        self.label_project_name.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_project_name, 0, 0, 1, 1)

        self.stackedWidget_path = QStackedWidget(self.page)
        self.stackedWidget_path.setObjectName(u"stackedWidget_path")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.stackedWidget_path.sizePolicy().hasHeightForWidth())
        self.stackedWidget_path.setSizePolicy(sizePolicy2)
        self.stackedWidget_path.setMaximumSize(QSize(16777215, 50))
        self.page_5 = QWidget()
        self.page_5.setObjectName(u"page_5")
        self.horizontalLayout_3 = QHBoxLayout(self.page_5)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_part = QLabel(self.page_5)
        self.label_part.setObjectName(u"label_part")

        self.horizontalLayout_3.addWidget(self.label_part)

        self.label_arrow_1 = QLabel(self.page_5)
        self.label_arrow_1.setObjectName(u"label_arrow_1")
        sizePolicy.setHeightForWidth(self.label_arrow_1.sizePolicy().hasHeightForWidth())
        self.label_arrow_1.setSizePolicy(sizePolicy)
        self.label_arrow_1.setMaximumSize(QSize(20, 16777215))

        self.horizontalLayout_3.addWidget(self.label_arrow_1)

        self.label_detail = QLabel(self.page_5)
        self.label_detail.setObjectName(u"label_detail")

        self.horizontalLayout_3.addWidget(self.label_detail)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_6)

        self.stackedWidget_path.addWidget(self.page_5)
        self.page_3 = QWidget()
        self.page_3.setObjectName(u"page_3")
        self.horizontalLayout_8 = QHBoxLayout(self.page_3)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.label_asset_type = QLabel(self.page_3)
        self.label_asset_type.setObjectName(u"label_asset_type")

        self.horizontalLayout_8.addWidget(self.label_asset_type)

        self.label_arrow_2 = QLabel(self.page_3)
        self.label_arrow_2.setObjectName(u"label_arrow_2")

        self.horizontalLayout_8.addWidget(self.label_arrow_2)

        self.label_asset = QLabel(self.page_3)
        self.label_asset.setObjectName(u"label_asset")

        self.horizontalLayout_8.addWidget(self.label_asset)

        self.label_arrow_3 = QLabel(self.page_3)
        self.label_arrow_3.setObjectName(u"label_arrow_3")

        self.horizontalLayout_8.addWidget(self.label_arrow_3)

        self.label_asset_task = QLabel(self.page_3)
        self.label_asset_task.setObjectName(u"label_asset_task")

        self.horizontalLayout_8.addWidget(self.label_asset_task)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_5)

        self.stackedWidget_path.addWidget(self.page_3)
        self.page_4 = QWidget()
        self.page_4.setObjectName(u"page_4")
        self.horizontalLayout_9 = QHBoxLayout(self.page_4)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.label_seq = QLabel(self.page_4)
        self.label_seq.setObjectName(u"label_seq")

        self.horizontalLayout_9.addWidget(self.label_seq)

        self.label_arrow_4 = QLabel(self.page_4)
        self.label_arrow_4.setObjectName(u"label_arrow_4")

        self.horizontalLayout_9.addWidget(self.label_arrow_4)

        self.label_shot = QLabel(self.page_4)
        self.label_shot.setObjectName(u"label_shot")

        self.horizontalLayout_9.addWidget(self.label_shot)

        self.label_arrow_5 = QLabel(self.page_4)
        self.label_arrow_5.setObjectName(u"label_arrow_5")

        self.horizontalLayout_9.addWidget(self.label_arrow_5)

        self.label_shot_task = QLabel(self.page_4)
        self.label_shot_task.setObjectName(u"label_shot_task")

        self.horizontalLayout_9.addWidget(self.label_shot_task)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer)

        self.stackedWidget_path.addWidget(self.page_4)

        self.gridLayout_2.addWidget(self.stackedWidget_path, 0, 1, 1, 1)

        self.tabWidget_pathtree = QTabWidget(self.page)
        self.tabWidget_pathtree.setObjectName(u"tabWidget_pathtree")
        self.tabWidget_pathtree.setMinimumSize(QSize(300, 0))
        self.tabWidget_pathtree.setMaximumSize(QSize(300, 16777215))
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.verticalLayout_6 = QVBoxLayout(self.tab)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.horizontalLayout_14.setContentsMargins(-1, -1, -1, 0)
        self.comboBox_filter = QComboBox(self.tab)
        self.comboBox_filter.setObjectName(u"comboBox_filter")

        self.horizontalLayout_14.addWidget(self.comboBox_filter)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_14.addItem(self.horizontalSpacer_7)


        self.verticalLayout_6.addLayout(self.horizontalLayout_14)

        self.lineEdit_search_my_tasks = QLineEdit(self.tab)
        self.lineEdit_search_my_tasks.setObjectName(u"lineEdit_search_my_tasks")

        self.verticalLayout_6.addWidget(self.lineEdit_search_my_tasks)

        self.treeWidget_my_tasks = QTreeWidget(self.tab)
        __qtreewidgetitem1 = QTreeWidgetItem()
        __qtreewidgetitem1.setText(0, u"1");
        self.treeWidget_my_tasks.setHeaderItem(__qtreewidgetitem1)
        self.treeWidget_my_tasks.setObjectName(u"treeWidget_my_tasks")
        sizePolicy1.setHeightForWidth(self.treeWidget_my_tasks.sizePolicy().hasHeightForWidth())
        self.treeWidget_my_tasks.setSizePolicy(sizePolicy1)
        self.treeWidget_my_tasks.setMinimumSize(QSize(0, 0))
        self.treeWidget_my_tasks.setMaximumSize(QSize(16777215, 16777215))
        self.treeWidget_my_tasks.header().setVisible(False)

        self.verticalLayout_6.addWidget(self.treeWidget_my_tasks)

        self.tabWidget_pathtree.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.verticalLayout_7 = QVBoxLayout(self.tab_2)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.lineEdit_search_assets = QLineEdit(self.tab_2)
        self.lineEdit_search_assets.setObjectName(u"lineEdit_search_assets")

        self.verticalLayout_7.addWidget(self.lineEdit_search_assets)

        self.treeWidget_assets = QTreeWidget(self.tab_2)
        __qtreewidgetitem2 = QTreeWidgetItem()
        __qtreewidgetitem2.setText(0, u"1");
        self.treeWidget_assets.setHeaderItem(__qtreewidgetitem2)
        self.treeWidget_assets.setObjectName(u"treeWidget_assets")
        self.treeWidget_assets.header().setVisible(False)

        self.verticalLayout_7.addWidget(self.treeWidget_assets)

        self.frame = QFrame(self.tab_2)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_10 = QVBoxLayout(self.frame)
        self.verticalLayout_10.setSpacing(0)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.checkBox_mod = QCheckBox(self.frame)
        self.checkBox_mod.setObjectName(u"checkBox_mod")

        self.verticalLayout_10.addWidget(self.checkBox_mod)

        self.checkBox_rig = QCheckBox(self.frame)
        self.checkBox_rig.setObjectName(u"checkBox_rig")

        self.verticalLayout_10.addWidget(self.checkBox_rig)

        self.checkBox_lkd = QCheckBox(self.frame)
        self.checkBox_lkd.setObjectName(u"checkBox_lkd")

        self.verticalLayout_10.addWidget(self.checkBox_lkd)

        self.horizontalLayout_20 = QHBoxLayout()
        self.horizontalLayout_20.setObjectName(u"horizontalLayout_20")
        self.horizontalLayout_20.setContentsMargins(-1, -1, -1, 0)
        self.pushButton_assets_all = QPushButton(self.frame)
        self.pushButton_assets_all.setObjectName(u"pushButton_assets_all")

        self.horizontalLayout_20.addWidget(self.pushButton_assets_all)

        self.pushButton_assets_none = QPushButton(self.frame)
        self.pushButton_assets_none.setObjectName(u"pushButton_assets_none")

        self.horizontalLayout_20.addWidget(self.pushButton_assets_none)


        self.verticalLayout_10.addLayout(self.horizontalLayout_20)


        self.verticalLayout_7.addWidget(self.frame)

        self.tabWidget_pathtree.addTab(self.tab_2, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.verticalLayout_8 = QVBoxLayout(self.tab_3)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.lineEdit_search_shots = QLineEdit(self.tab_3)
        self.lineEdit_search_shots.setObjectName(u"lineEdit_search_shots")

        self.verticalLayout_8.addWidget(self.lineEdit_search_shots)

        self.treeWidget_shots = QTreeWidget(self.tab_3)
        __qtreewidgetitem3 = QTreeWidgetItem()
        __qtreewidgetitem3.setText(0, u"1");
        self.treeWidget_shots.setHeaderItem(__qtreewidgetitem3)
        self.treeWidget_shots.setObjectName(u"treeWidget_shots")
        self.treeWidget_shots.header().setVisible(False)

        self.verticalLayout_8.addWidget(self.treeWidget_shots)

        self.frame_2 = QFrame(self.tab_3)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frame_2)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.checkBox_ani = QCheckBox(self.frame_2)
        self.checkBox_ani.setObjectName(u"checkBox_ani")

        self.verticalLayout_3.addWidget(self.checkBox_ani)

        self.checkBox_lgt = QCheckBox(self.frame_2)
        self.checkBox_lgt.setObjectName(u"checkBox_lgt")

        self.verticalLayout_3.addWidget(self.checkBox_lgt)

        self.checkBox_cmp = QCheckBox(self.frame_2)
        self.checkBox_cmp.setObjectName(u"checkBox_cmp")

        self.verticalLayout_3.addWidget(self.checkBox_cmp)

        self.checkBox_mm = QCheckBox(self.frame_2)
        self.checkBox_mm.setObjectName(u"checkBox_mm")

        self.verticalLayout_3.addWidget(self.checkBox_mm)

        self.checkBox_ly = QCheckBox(self.frame_2)
        self.checkBox_ly.setObjectName(u"checkBox_ly")

        self.verticalLayout_3.addWidget(self.checkBox_ly)

        self.checkBox_fx = QCheckBox(self.frame_2)
        self.checkBox_fx.setObjectName(u"checkBox_fx")

        self.verticalLayout_3.addWidget(self.checkBox_fx)

        self.horizontalLayout_16 = QHBoxLayout()
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.horizontalLayout_16.setContentsMargins(-1, -1, -1, 0)
        self.pushButton_shots_all = QPushButton(self.frame_2)
        self.pushButton_shots_all.setObjectName(u"pushButton_shots_all")

        self.horizontalLayout_16.addWidget(self.pushButton_shots_all)

        self.pushButton_shots_none = QPushButton(self.frame_2)
        self.pushButton_shots_none.setObjectName(u"pushButton_shots_none")

        self.horizontalLayout_16.addWidget(self.pushButton_shots_none)


        self.verticalLayout_3.addLayout(self.horizontalLayout_16)


        self.verticalLayout_8.addWidget(self.frame_2)

        self.tabWidget_pathtree.addTab(self.tab_3, "")

        self.gridLayout_2.addWidget(self.tabWidget_pathtree, 1, 0, 1, 1)


        self.verticalLayout_11.addLayout(self.gridLayout_2)

        self.verticalSpacer = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_11.addItem(self.verticalSpacer)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setVerticalSpacing(4)
        self.gridLayout.setContentsMargins(-1, -1, -1, 0)
        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.comboBox_filetype = QComboBox(self.page)
        self.comboBox_filetype.setObjectName(u"comboBox_filetype")

        self.horizontalLayout_11.addWidget(self.comboBox_filetype)

        self.horizontalSpacer_4 = QSpacerItem(600, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_11.addItem(self.horizontalSpacer_4)


        self.gridLayout.addLayout(self.horizontalLayout_11, 2, 2, 1, 1)

        self.label_89 = QLabel(self.page)
        self.label_89.setObjectName(u"label_89")
        sizePolicy1.setHeightForWidth(self.label_89.sizePolicy().hasHeightForWidth())
        self.label_89.setSizePolicy(sizePolicy1)
        self.label_89.setMinimumSize(QSize(80, 20))
        self.label_89.setMaximumSize(QSize(80, 20))
        self.label_89.setFont(font1)
        self.label_89.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_89, 5, 0, 1, 1, Qt.AlignRight)

        self.horizontalSpacer_13 = QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_13, 0, 1, 1, 1)

        self.label_85 = QLabel(self.page)
        self.label_85.setObjectName(u"label_85")
        sizePolicy1.setHeightForWidth(self.label_85.sizePolicy().hasHeightForWidth())
        self.label_85.setSizePolicy(sizePolicy1)
        self.label_85.setMinimumSize(QSize(80, 20))
        self.label_85.setMaximumSize(QSize(80, 20))
        self.label_85.setFont(font1)
        self.label_85.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_85, 2, 0, 1, 1, Qt.AlignRight)

        self.verticalSpacer_2 = QSpacerItem(20, 15, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.gridLayout.addItem(self.verticalSpacer_2, 3, 0, 1, 1)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.spinBox_version = QSpinBox(self.page)
        self.spinBox_version.setObjectName(u"spinBox_version")
        self.spinBox_version.setMinimumSize(QSize(60, 0))

        self.horizontalLayout_4.addWidget(self.spinBox_version)

        self.horizontalSpacer_12 = QSpacerItem(10, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_12)

        self.checkBox_avaliable_ver = QCheckBox(self.page)
        self.checkBox_avaliable_ver.setObjectName(u"checkBox_avaliable_ver")

        self.horizontalLayout_4.addWidget(self.checkBox_avaliable_ver)

        self.horizontalSpacer_3 = QSpacerItem(460, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_3)


        self.gridLayout.addLayout(self.horizontalLayout_4, 1, 2, 1, 1)

        self.label_82 = QLabel(self.page)
        self.label_82.setObjectName(u"label_82")
        sizePolicy1.setHeightForWidth(self.label_82.sizePolicy().hasHeightForWidth())
        self.label_82.setSizePolicy(sizePolicy1)
        self.label_82.setMinimumSize(QSize(80, 20))
        self.label_82.setMaximumSize(QSize(80, 20))
        self.label_82.setFont(font1)
        self.label_82.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_82, 1, 0, 1, 1, Qt.AlignRight)

        self.label_preview = QLabel(self.page)
        self.label_preview.setObjectName(u"label_preview")

        self.gridLayout.addWidget(self.label_preview, 4, 2, 1, 1)

        self.label_3 = QLabel(self.page)
        self.label_3.setObjectName(u"label_3")
        sizePolicy1.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy1)
        self.label_3.setMinimumSize(QSize(80, 20))
        self.label_3.setMaximumSize(QSize(80, 20))
        self.label_3.setFont(font1)
        self.label_3.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1, Qt.AlignRight)

        self.label_87 = QLabel(self.page)
        self.label_87.setObjectName(u"label_87")
        sizePolicy1.setHeightForWidth(self.label_87.sizePolicy().hasHeightForWidth())
        self.label_87.setSizePolicy(sizePolicy1)
        self.label_87.setMinimumSize(QSize(80, 20))
        self.label_87.setMaximumSize(QSize(80, 20))
        self.label_87.setFont(font1)
        self.label_87.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_87, 4, 0, 1, 1, Qt.AlignRight)

        self.label_new_file_name = QLabel(self.page)
        self.label_new_file_name.setObjectName(u"label_new_file_name")

        self.gridLayout.addWidget(self.label_new_file_name, 0, 2, 1, 1)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(-1, -1, -1, 0)
        self.label_work_area = QLabel(self.page)
        self.label_work_area.setObjectName(u"label_work_area")

        self.horizontalLayout_5.addWidget(self.label_work_area)

        self.checkBox_avaliable_path = QCheckBox(self.page)
        self.checkBox_avaliable_path.setObjectName(u"checkBox_avaliable_path")

        self.horizontalLayout_5.addWidget(self.checkBox_avaliable_path, 0, Qt.AlignRight)


        self.gridLayout.addLayout(self.horizontalLayout_5, 5, 2, 1, 1)


        self.verticalLayout_11.addLayout(self.gridLayout)

        self.horizontalLayout_19 = QHBoxLayout()
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.horizontalLayout_19.setContentsMargins(10, -1, -1, 0)
        self.label_validate_path = QLabel(self.page)
        self.label_validate_path.setObjectName(u"label_validate_path")
        font2 = QFont()
        font2.setBold(False)
        self.label_validate_path.setFont(font2)
        self.label_validate_path.setStyleSheet(u"color: rgb(239, 41, 41);")

        self.horizontalLayout_19.addWidget(self.label_validate_path)

        self.horizontalSpacer_10 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_19.addItem(self.horizontalSpacer_10)

        self.pushButton_cancel = QPushButton(self.page)
        self.pushButton_cancel.setObjectName(u"pushButton_cancel")

        self.horizontalLayout_19.addWidget(self.pushButton_cancel)

        self.pushButton_save = QPushButton(self.page)
        self.pushButton_save.setObjectName(u"pushButton_save")

        self.horizontalLayout_19.addWidget(self.pushButton_save)


        self.verticalLayout_11.addLayout(self.horizontalLayout_19)

        self.stackedWidget.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.horizontalLayout_6 = QHBoxLayout(self.page_2)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.frame_3 = QFrame(self.page_2)
        self.frame_3.setObjectName(u"frame_3")
        sizePolicy.setHeightForWidth(self.frame_3.sizePolicy().hasHeightForWidth())
        self.frame_3.setSizePolicy(sizePolicy)
        self.frame_3.setMaximumSize(QSize(300, 16777215))
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.frame_3)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_main_icon = QLabel(self.frame_3)
        self.label_main_icon.setObjectName(u"label_main_icon")
        sizePolicy1.setHeightForWidth(self.label_main_icon.sizePolicy().hasHeightForWidth())
        self.label_main_icon.setSizePolicy(sizePolicy1)
        self.label_main_icon.setMinimumSize(QSize(100, 100))
        self.label_main_icon.setMaximumSize(QSize(100, 100))

        self.verticalLayout.addWidget(self.label_main_icon)

        self.label_4 = QLabel(self.frame_3)
        self.label_4.setObjectName(u"label_4")
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setMaximumSize(QSize(16777215, 16777215))
        font3 = QFont()
        font3.setPointSize(12)
        font3.setBold(True)
        self.label_4.setFont(font3)

        self.verticalLayout.addWidget(self.label_4)

        self.label_5 = QLabel(self.frame_3)
        self.label_5.setObjectName(u"label_5")
        font4 = QFont()
        font4.setPointSize(40)
        font4.setBold(True)
        self.label_5.setFont(font4)

        self.verticalLayout.addWidget(self.label_5)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout.addItem(self.verticalSpacer_4)

        self.label_6 = QLabel(self.frame_3)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setWordWrap(True)

        self.verticalLayout.addWidget(self.label_6)

        self.verticalSpacer_5 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout.addItem(self.verticalSpacer_5)

        self.label_7 = QLabel(self.frame_3)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setWordWrap(True)

        self.verticalLayout.addWidget(self.label_7)

        self.verticalSpacer_6 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout.addItem(self.verticalSpacer_6)

        self.label_8 = QLabel(self.frame_3)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setWordWrap(True)

        self.verticalLayout.addWidget(self.label_8)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout.addItem(self.verticalSpacer_3)

        self.label_print_status = QLabel(self.frame_3)
        self.label_print_status.setObjectName(u"label_print_status")
        sizePolicy.setHeightForWidth(self.label_print_status.sizePolicy().hasHeightForWidth())
        self.label_print_status.setSizePolicy(sizePolicy)
        self.label_print_status.setMinimumSize(QSize(0, 200))
        self.label_print_status.setMaximumSize(QSize(16777215, 200))
        self.label_print_status.setWordWrap(True)

        self.verticalLayout.addWidget(self.label_print_status)

        self.verticalSpacer_7 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_7)


        self.horizontalLayout_6.addWidget(self.frame_3)

        self.label_gif = QLabel(self.page_2)
        self.label_gif.setObjectName(u"label_gif")

        self.horizontalLayout_6.addWidget(self.label_gif, 0, Qt.AlignHCenter)

        self.stackedWidget.addWidget(self.page_2)

        self.horizontalLayout_2.addWidget(self.stackedWidget)


        self.retranslateUi(Form)

        self.stackedWidget.setCurrentIndex(0)
        self.tabWidget_file_list.setCurrentIndex(1)
        self.stackedWidget_path.setCurrentIndex(0)
        self.tabWidget_pathtree.setCurrentIndex(2)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label_icon.setText("")
        self.label.setText(QCoreApplication.translate("Form", u"File Save", None))
        self.label_user_name.setText(QCoreApplication.translate("Form", u"User Name", None))
        self.label_user_icon.setText("")
        self.tabWidget_file_list.setTabText(self.tabWidget_file_list.indexOf(self.tab_4), QCoreApplication.translate("Form", u"All", None))
        self.tabWidget_file_list.setTabText(self.tabWidget_file_list.indexOf(self.tab_5), QCoreApplication.translate("Form", u"Working", None))
        self.tabWidget_file_list.setTabText(self.tabWidget_file_list.indexOf(self.tab_6), QCoreApplication.translate("Form", u"Publishes", None))
        self.label_project_name.setText(QCoreApplication.translate("Form", u"Project Name", None))
        self.label_part.setText(QCoreApplication.translate("Form", u"My Tasks", None))
        self.label_arrow_1.setText(QCoreApplication.translate("Form", u"\u25b6", None))
        self.label_detail.setText(QCoreApplication.translate("Form", u"Task test", None))
        self.label_asset_type.setText(QCoreApplication.translate("Form", u"Asset Type", None))
        self.label_arrow_2.setText(QCoreApplication.translate("Form", u"\u25b6", None))
        self.label_asset.setText(QCoreApplication.translate("Form", u"Asset", None))
        self.label_arrow_3.setText(QCoreApplication.translate("Form", u"\u25b6", None))
        self.label_asset_task.setText(QCoreApplication.translate("Form", u"Task", None))
        self.label_seq.setText(QCoreApplication.translate("Form", u"Sequence", None))
        self.label_arrow_4.setText(QCoreApplication.translate("Form", u"\u25b6", None))
        self.label_shot.setText(QCoreApplication.translate("Form", u"Shot", None))
        self.label_arrow_5.setText(QCoreApplication.translate("Form", u"\u25b6", None))
        self.label_shot_task.setText(QCoreApplication.translate("Form", u"Task", None))
        self.tabWidget_pathtree.setTabText(self.tabWidget_pathtree.indexOf(self.tab), QCoreApplication.translate("Form", u"My Tasks", None))
        self.checkBox_mod.setText(QCoreApplication.translate("Form", u"Modeling", None))
        self.checkBox_rig.setText(QCoreApplication.translate("Form", u"Rig", None))
        self.checkBox_lkd.setText(QCoreApplication.translate("Form", u"LookDev", None))
        self.pushButton_assets_all.setText(QCoreApplication.translate("Form", u"Select All", None))
        self.pushButton_assets_none.setText(QCoreApplication.translate("Form", u"Select None", None))
        self.tabWidget_pathtree.setTabText(self.tabWidget_pathtree.indexOf(self.tab_2), QCoreApplication.translate("Form", u"Assets", None))
        self.checkBox_ani.setText(QCoreApplication.translate("Form", u"Animation", None))
        self.checkBox_lgt.setText(QCoreApplication.translate("Form", u"Lighting", None))
        self.checkBox_cmp.setText(QCoreApplication.translate("Form", u"Compositing", None))
        self.checkBox_mm.setText(QCoreApplication.translate("Form", u"Matchmove", None))
        self.checkBox_ly.setText(QCoreApplication.translate("Form", u"Layout", None))
        self.checkBox_fx.setText(QCoreApplication.translate("Form", u"FX", None))
        self.pushButton_shots_all.setText(QCoreApplication.translate("Form", u"Select All", None))
        self.pushButton_shots_none.setText(QCoreApplication.translate("Form", u"Select None", None))
        self.tabWidget_pathtree.setTabText(self.tabWidget_pathtree.indexOf(self.tab_3), QCoreApplication.translate("Form", u"Shots", None))
        self.label_89.setText(QCoreApplication.translate("Form", u"Work Area", None))
        self.label_85.setText(QCoreApplication.translate("Form", u"File Type", None))
        self.checkBox_avaliable_ver.setText(QCoreApplication.translate("Form", u"Use next Avaliable Version number", None))
        self.label_82.setText(QCoreApplication.translate("Form", u"Version", None))
        self.label_preview.setText("")
        self.label_3.setText(QCoreApplication.translate("Form", u"Name", None))
        self.label_87.setText(QCoreApplication.translate("Form", u"Preview", None))
        self.label_new_file_name.setText("")
        self.label_work_area.setText("")
        self.checkBox_avaliable_path.setText(QCoreApplication.translate("Form", u"Set Work Area According to Current File Information", None))
        self.label_validate_path.setText(QCoreApplication.translate("Form", u"\u25a0 The save path is not valid. ", None))
        self.pushButton_cancel.setText(QCoreApplication.translate("Form", u"Cancel", None))
        self.pushButton_save.setText(QCoreApplication.translate("Form", u"Save", None))
        self.label_main_icon.setText(QCoreApplication.translate("Form", u"TextLabel", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"\n"
"Made by Team", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"Phoenix", None))
        self.label_6.setText(QCoreApplication.translate("Form", u"Work period from August 14, 2024, to September 4, 2024", None))
        self.label_7.setText(QCoreApplication.translate("Form", u"Created by Wonjin Lee, Seyoung Kang, Sunjin Yoon, Yumi Kang, and Gyeoul Kim", None))
        self.label_8.setText(QCoreApplication.translate("Form", u"Thanks to master Seonil Hong and Netflix 4th Academy. We have worked hard on this, so even though it may not be perfect, I hope you'll find it enjoyable.", None))
        self.label_print_status.setText("")
        self.label_gif.setText(QCoreApplication.translate("Form", u"TextLabel", None))
    # retranslateUi

