# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'loader_mockup_v5kDDPwC.ui'
##
## Created by: Qt User Interface Compiler version 6.2.4
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QHBoxLayout,
    QHeaderView, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QSpacerItem, QStackedWidget, QTabWidget,
    QTableWidget, QTableWidgetItem, QTreeWidget, QTreeWidgetItem,
    QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(950, 743)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(20, -1, 20, 0)
        self.label = QLabel(Form)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(22)
        font.setBold(True)
        self.label.setFont(font)

        self.horizontalLayout.addWidget(self.label, 0, Qt.AlignLeft)

        self.label_username = QLabel(Form)
        self.label_username.setObjectName(u"label_username")

        self.horizontalLayout.addWidget(self.label_username, 0, Qt.AlignRight)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.stackedWidget_main = QStackedWidget(Form)
        self.stackedWidget_main.setObjectName(u"stackedWidget_main")
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.verticalLayout_2 = QVBoxLayout(self.page)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(10, -1, 10, 0)
        self.label_3 = QLabel(self.page)
        self.label_3.setObjectName(u"label_3")
        font1 = QFont()
        font1.setPointSize(18)
        self.label_3.setFont(font1)

        self.verticalLayout_3.addWidget(self.label_3)

        self.tableWidget_home_projects = QTableWidget(self.page)
        self.tableWidget_home_projects.setObjectName(u"tableWidget_home_projects")

        self.verticalLayout_3.addWidget(self.tableWidget_home_projects)


        self.verticalLayout_2.addLayout(self.verticalLayout_3)

        self.stackedWidget_main.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.verticalLayout_4 = QVBoxLayout(self.page_2)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.stackedWidget_path = QStackedWidget(self.page_2)
        self.stackedWidget_path.setObjectName(u"stackedWidget_path")
        self.page_5 = QWidget()
        self.page_5.setObjectName(u"page_5")
        self.stackedWidget_path.addWidget(self.page_5)
        self.page_3 = QWidget()
        self.page_3.setObjectName(u"page_3")
        self.horizontalLayout_8 = QHBoxLayout(self.page_3)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.label_asset = QLabel(self.page_3)
        self.label_asset.setObjectName(u"label_asset")

        self.horizontalLayout_8.addWidget(self.label_asset)

        self.label_10 = QLabel(self.page_3)
        self.label_10.setObjectName(u"label_10")

        self.horizontalLayout_8.addWidget(self.label_10)

        self.label_env = QLabel(self.page_3)
        self.label_env.setObjectName(u"label_env")

        self.horizontalLayout_8.addWidget(self.label_env)

        self.label_8 = QLabel(self.page_3)
        self.label_8.setObjectName(u"label_8")

        self.horizontalLayout_8.addWidget(self.label_8)

        self.label_mod = QLabel(self.page_3)
        self.label_mod.setObjectName(u"label_mod")

        self.horizontalLayout_8.addWidget(self.label_mod)

        self.stackedWidget_path.addWidget(self.page_3)
        self.page_4 = QWidget()
        self.page_4.setObjectName(u"page_4")
        self.horizontalLayout_9 = QHBoxLayout(self.page_4)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.label_seq = QLabel(self.page_4)
        self.label_seq.setObjectName(u"label_seq")

        self.horizontalLayout_9.addWidget(self.label_seq)

        self.label_15 = QLabel(self.page_4)
        self.label_15.setObjectName(u"label_15")

        self.horizontalLayout_9.addWidget(self.label_15)

        self.label_shot = QLabel(self.page_4)
        self.label_shot.setObjectName(u"label_shot")

        self.horizontalLayout_9.addWidget(self.label_shot)

        self.label_13 = QLabel(self.page_4)
        self.label_13.setObjectName(u"label_13")

        self.horizontalLayout_9.addWidget(self.label_13)

        self.label_ani = QLabel(self.page_4)
        self.label_ani.setObjectName(u"label_ani")

        self.horizontalLayout_9.addWidget(self.label_ani)

        self.stackedWidget_path.addWidget(self.page_4)

        self.horizontalLayout_7.addWidget(self.stackedWidget_path)

        self.lineEdit_ver_search = QLineEdit(self.page_2)
        self.lineEdit_ver_search.setObjectName(u"lineEdit_ver_search")
        self.lineEdit_ver_search.setMaximumSize(QSize(200, 16777215))

        self.horizontalLayout_7.addWidget(self.lineEdit_ver_search)

        self.pushButton_grid = QPushButton(self.page_2)
        self.pushButton_grid.setObjectName(u"pushButton_grid")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_grid.sizePolicy().hasHeightForWidth())
        self.pushButton_grid.setSizePolicy(sizePolicy)
        self.pushButton_grid.setMinimumSize(QSize(50, 50))
        self.pushButton_grid.setMaximumSize(QSize(50, 50))

        self.horizontalLayout_7.addWidget(self.pushButton_grid)

        self.pushButton_list = QPushButton(self.page_2)
        self.pushButton_list.setObjectName(u"pushButton_list")
        sizePolicy.setHeightForWidth(self.pushButton_list.sizePolicy().hasHeightForWidth())
        self.pushButton_list.setSizePolicy(sizePolicy)
        self.pushButton_list.setMinimumSize(QSize(50, 50))
        self.pushButton_list.setMaximumSize(QSize(50, 50))

        self.horizontalLayout_7.addWidget(self.pushButton_list)


        self.gridLayout.addLayout(self.horizontalLayout_7, 0, 1, 1, 1)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(-1, 10, -1, 10)
        self.tabWidget = QTabWidget(self.page_2)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setMinimumSize(QSize(300, 0))
        self.tabWidget.setMaximumSize(QSize(300, 16777215))
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.verticalLayout_6 = QVBoxLayout(self.tab)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.lineEdit_tasks_search = QLineEdit(self.tab)
        self.lineEdit_tasks_search.setObjectName(u"lineEdit_tasks_search")

        self.verticalLayout_6.addWidget(self.lineEdit_tasks_search)

        self.treeWidget_pathtree = QTreeWidget(self.tab)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"1");
        self.treeWidget_pathtree.setHeaderItem(__qtreewidgetitem)
        self.treeWidget_pathtree.setObjectName(u"treeWidget_pathtree")
        self.treeWidget_pathtree.header().setVisible(False)

        self.verticalLayout_6.addWidget(self.treeWidget_pathtree)

        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.verticalLayout_7 = QVBoxLayout(self.tab_2)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.lineEdit_assets_search = QLineEdit(self.tab_2)
        self.lineEdit_assets_search.setObjectName(u"lineEdit_assets_search")

        self.verticalLayout_7.addWidget(self.lineEdit_assets_search)

        self.treeWidget_Assets = QTreeWidget(self.tab_2)
        __qtreewidgetitem1 = QTreeWidgetItem()
        __qtreewidgetitem1.setText(0, u"1");
        self.treeWidget_Assets.setHeaderItem(__qtreewidgetitem1)
        self.treeWidget_Assets.setObjectName(u"treeWidget_Assets")
        self.treeWidget_Assets.header().setVisible(False)

        self.verticalLayout_7.addWidget(self.treeWidget_Assets)

        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.verticalLayout_8 = QVBoxLayout(self.tab_3)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.lineEdit_shots_search = QLineEdit(self.tab_3)
        self.lineEdit_shots_search.setObjectName(u"lineEdit_shots_search")

        self.verticalLayout_8.addWidget(self.lineEdit_shots_search)

        self.treeWidget_3 = QTreeWidget(self.tab_3)
        __qtreewidgetitem2 = QTreeWidgetItem()
        __qtreewidgetitem2.setText(0, u"1");
        self.treeWidget_3.setHeaderItem(__qtreewidgetitem2)
        self.treeWidget_3.setObjectName(u"treeWidget_3")
        self.treeWidget_3.header().setVisible(False)

        self.verticalLayout_8.addWidget(self.treeWidget_3)

        self.tabWidget.addTab(self.tab_3, "")

        self.verticalLayout_5.addWidget(self.tabWidget)


        self.gridLayout.addLayout(self.verticalLayout_5, 1, 0, 1, 1)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(-1, -1, -1, 0)
        self.pushButton_home = QPushButton(self.page_2)
        self.pushButton_home.setObjectName(u"pushButton_home")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.pushButton_home.sizePolicy().hasHeightForWidth())
        self.pushButton_home.setSizePolicy(sizePolicy1)
        self.pushButton_home.setMinimumSize(QSize(50, 50))
        self.pushButton_home.setMaximumSize(QSize(50, 50))

        self.horizontalLayout_6.addWidget(self.pushButton_home)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer)

        self.label_project_name = QLabel(self.page_2)
        self.label_project_name.setObjectName(u"label_project_name")
        font2 = QFont()
        font2.setBold(True)
        self.label_project_name.setFont(font2)

        self.horizontalLayout_6.addWidget(self.label_project_name)


        self.gridLayout.addLayout(self.horizontalLayout_6, 0, 0, 1, 1)

        self.stackedWidget_sub = QStackedWidget(self.page_2)
        self.stackedWidget_sub.setObjectName(u"stackedWidget_sub")
        sizePolicy.setHeightForWidth(self.stackedWidget_sub.sizePolicy().hasHeightForWidth())
        self.stackedWidget_sub.setSizePolicy(sizePolicy)
        self.stackedWidget_sub.setMinimumSize(QSize(600, 600))
        self.stackedWidget_sub.setMaximumSize(QSize(600, 600))
        self.stackedWidget_sub.setStyleSheet(u"")
        self.stackedWidget_sub.setFrameShape(QFrame.NoFrame)
        self.stackedWidget_sub.setFrameShadow(QFrame.Plain)
        self.stackedWidget_sub.setLineWidth(1)
        self.page_6 = QWidget()
        self.page_6.setObjectName(u"page_6")
        self.verticalLayout_9 = QVBoxLayout(self.page_6)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.tabWidget_grid_full_wip = QTabWidget(self.page_6)
        self.tabWidget_grid_full_wip.setObjectName(u"tabWidget_grid_full_wip")
        self.tab_4 = QWidget()
        self.tab_4.setObjectName(u"tab_4")
        self.verticalLayout_16 = QVBoxLayout(self.tab_4)
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.pushButton_new_wip_1 = QPushButton(self.tab_4)
        self.pushButton_new_wip_1.setObjectName(u"pushButton_new_wip_1")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.pushButton_new_wip_1.sizePolicy().hasHeightForWidth())
        self.pushButton_new_wip_1.setSizePolicy(sizePolicy2)
        self.pushButton_new_wip_1.setMinimumSize(QSize(200, 0))
        self.pushButton_new_wip_1.setMaximumSize(QSize(200, 16777215))

        self.verticalLayout_16.addWidget(self.pushButton_new_wip_1, 0, Qt.AlignRight)

        self.tableWidget_grid_full = QTableWidget(self.tab_4)
        self.tableWidget_grid_full.setObjectName(u"tableWidget_grid_full")

        self.verticalLayout_16.addWidget(self.tableWidget_grid_full)

        self.tabWidget_grid_full_wip.addTab(self.tab_4, "")
        self.tab_5 = QWidget()
        self.tab_5.setObjectName(u"tab_5")
        self.verticalLayout_17 = QVBoxLayout(self.tab_5)
        self.verticalLayout_17.setObjectName(u"verticalLayout_17")
        self.pushButton_new_pub_1 = QPushButton(self.tab_5)
        self.pushButton_new_pub_1.setObjectName(u"pushButton_new_pub_1")
        self.pushButton_new_pub_1.setMinimumSize(QSize(200, 0))
        self.pushButton_new_pub_1.setMaximumSize(QSize(200, 16777215))

        self.verticalLayout_17.addWidget(self.pushButton_new_pub_1, 0, Qt.AlignRight)

        self.tableWidget_grid_full_pub = QTableWidget(self.tab_5)
        self.tableWidget_grid_full_pub.setObjectName(u"tableWidget_grid_full_pub")

        self.verticalLayout_17.addWidget(self.tableWidget_grid_full_pub)

        self.tabWidget_grid_full_wip.addTab(self.tab_5, "")

        self.verticalLayout_9.addWidget(self.tabWidget_grid_full_wip)

        self.stackedWidget_sub.addWidget(self.page_6)
        self.page_7 = QWidget()
        self.page_7.setObjectName(u"page_7")
        self.verticalLayout_10 = QVBoxLayout(self.page_7)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.tabWidget_2 = QTabWidget(self.page_7)
        self.tabWidget_2.setObjectName(u"tabWidget_2")
        self.tab_6 = QWidget()
        self.tab_6.setObjectName(u"tab_6")
        self.verticalLayout_19 = QVBoxLayout(self.tab_6)
        self.verticalLayout_19.setObjectName(u"verticalLayout_19")
        self.pushButton_new_wip_2 = QPushButton(self.tab_6)
        self.pushButton_new_wip_2.setObjectName(u"pushButton_new_wip_2")
        sizePolicy2.setHeightForWidth(self.pushButton_new_wip_2.sizePolicy().hasHeightForWidth())
        self.pushButton_new_wip_2.setSizePolicy(sizePolicy2)
        self.pushButton_new_wip_2.setMinimumSize(QSize(200, 0))
        self.pushButton_new_wip_2.setMaximumSize(QSize(200, 16777215))

        self.verticalLayout_19.addWidget(self.pushButton_new_wip_2, 0, Qt.AlignRight)

        self.tableWidget_grid_wip = QTableWidget(self.tab_6)
        self.tableWidget_grid_wip.setObjectName(u"tableWidget_grid_wip")

        self.verticalLayout_19.addWidget(self.tableWidget_grid_wip)

        self.tabWidget_2.addTab(self.tab_6, "")
        self.tab_7 = QWidget()
        self.tab_7.setObjectName(u"tab_7")
        self.verticalLayout_20 = QVBoxLayout(self.tab_7)
        self.verticalLayout_20.setObjectName(u"verticalLayout_20")
        self.pushButton_new_pub_2 = QPushButton(self.tab_7)
        self.pushButton_new_pub_2.setObjectName(u"pushButton_new_pub_2")
        sizePolicy2.setHeightForWidth(self.pushButton_new_pub_2.sizePolicy().hasHeightForWidth())
        self.pushButton_new_pub_2.setSizePolicy(sizePolicy2)
        self.pushButton_new_pub_2.setMinimumSize(QSize(200, 0))
        self.pushButton_new_pub_2.setMaximumSize(QSize(200, 16777215))

        self.verticalLayout_20.addWidget(self.pushButton_new_pub_2, 0, Qt.AlignRight)

        self.tableWidget_grid_pub = QTableWidget(self.tab_7)
        self.tableWidget_grid_pub.setObjectName(u"tableWidget_grid_pub")

        self.verticalLayout_20.addWidget(self.tableWidget_grid_pub)

        self.tabWidget_2.addTab(self.tab_7, "")

        self.verticalLayout_10.addWidget(self.tabWidget_2)

        self.frame = QFrame(self.page_7)
        self.frame.setObjectName(u"frame")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy3)
        self.frame.setMinimumSize(QSize(0, 250))
        self.frame.setMaximumSize(QSize(16777215, 250))
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_11 = QVBoxLayout(self.frame)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.stackedWidget_sub_grid = QStackedWidget(self.frame)
        self.stackedWidget_sub_grid.setObjectName(u"stackedWidget_sub_grid")
        self.page_8 = QWidget()
        self.page_8.setObjectName(u"page_8")
        self.verticalLayout_12 = QVBoxLayout(self.page_8)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.label_35 = QLabel(self.page_8)
        self.label_35.setObjectName(u"label_35")
        sizePolicy4 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.label_35.sizePolicy().hasHeightForWidth())
        self.label_35.setSizePolicy(sizePolicy4)
        self.label_35.setMinimumSize(QSize(100, 0))
        self.label_35.setMaximumSize(QSize(100, 16777215))

        self.gridLayout_3.addWidget(self.label_35, 1, 0, 1, 1)

        self.label_41 = QLabel(self.page_8)
        self.label_41.setObjectName(u"label_41")
        sizePolicy4.setHeightForWidth(self.label_41.sizePolicy().hasHeightForWidth())
        self.label_41.setSizePolicy(sizePolicy4)
        self.label_41.setMinimumSize(QSize(100, 0))
        self.label_41.setMaximumSize(QSize(100, 16777215))

        self.gridLayout_3.addWidget(self.label_41, 6, 0, 1, 1)

        self.label_grid_shot_name = QLabel(self.page_8)
        self.label_grid_shot_name.setObjectName(u"label_grid_shot_name")

        self.gridLayout_3.addWidget(self.label_grid_shot_name, 0, 1, 1, 1)

        self.label_37 = QLabel(self.page_8)
        self.label_37.setObjectName(u"label_37")
        sizePolicy4.setHeightForWidth(self.label_37.sizePolicy().hasHeightForWidth())
        self.label_37.setSizePolicy(sizePolicy4)
        self.label_37.setMinimumSize(QSize(100, 0))
        self.label_37.setMaximumSize(QSize(100, 16777215))

        self.gridLayout_3.addWidget(self.label_37, 2, 0, 1, 1)

        self.label_33 = QLabel(self.page_8)
        self.label_33.setObjectName(u"label_33")
        sizePolicy4.setHeightForWidth(self.label_33.sizePolicy().hasHeightForWidth())
        self.label_33.setSizePolicy(sizePolicy4)
        self.label_33.setMinimumSize(QSize(100, 0))
        self.label_33.setMaximumSize(QSize(100, 16777215))

        self.gridLayout_3.addWidget(self.label_33, 0, 0, 1, 1)

        self.label_grid_shot_ver = QLabel(self.page_8)
        self.label_grid_shot_ver.setObjectName(u"label_grid_shot_ver")

        self.gridLayout_3.addWidget(self.label_grid_shot_ver, 2, 1, 1, 1)

        self.label_grid_shot_artist = QLabel(self.page_8)
        self.label_grid_shot_artist.setObjectName(u"label_grid_shot_artist")

        self.gridLayout_3.addWidget(self.label_grid_shot_artist, 5, 1, 1, 1)

        self.label_grid_shot_type = QLabel(self.page_8)
        self.label_grid_shot_type.setObjectName(u"label_grid_shot_type")

        self.gridLayout_3.addWidget(self.label_grid_shot_type, 1, 1, 1, 1)

        self.label_39 = QLabel(self.page_8)
        self.label_39.setObjectName(u"label_39")
        sizePolicy4.setHeightForWidth(self.label_39.sizePolicy().hasHeightForWidth())
        self.label_39.setSizePolicy(sizePolicy4)
        self.label_39.setMinimumSize(QSize(100, 0))
        self.label_39.setMaximumSize(QSize(100, 16777215))

        self.gridLayout_3.addWidget(self.label_39, 4, 0, 1, 1)

        self.label_grid_shot_date = QLabel(self.page_8)
        self.label_grid_shot_date.setObjectName(u"label_grid_shot_date")

        self.gridLayout_3.addWidget(self.label_grid_shot_date, 4, 1, 1, 1)

        self.label_grid_shot_link = QLabel(self.page_8)
        self.label_grid_shot_link.setObjectName(u"label_grid_shot_link")

        self.gridLayout_3.addWidget(self.label_grid_shot_link, 3, 1, 1, 1)

        self.label_grid_shot_frame = QLabel(self.page_8)
        self.label_grid_shot_frame.setObjectName(u"label_grid_shot_frame")

        self.gridLayout_3.addWidget(self.label_grid_shot_frame, 6, 1, 1, 1)

        self.label_38 = QLabel(self.page_8)
        self.label_38.setObjectName(u"label_38")
        sizePolicy4.setHeightForWidth(self.label_38.sizePolicy().hasHeightForWidth())
        self.label_38.setSizePolicy(sizePolicy4)
        self.label_38.setMinimumSize(QSize(100, 0))
        self.label_38.setMaximumSize(QSize(100, 16777215))

        self.gridLayout_3.addWidget(self.label_38, 3, 0, 1, 1)

        self.label_40 = QLabel(self.page_8)
        self.label_40.setObjectName(u"label_40")
        sizePolicy4.setHeightForWidth(self.label_40.sizePolicy().hasHeightForWidth())
        self.label_40.setSizePolicy(sizePolicy4)
        self.label_40.setMinimumSize(QSize(100, 0))
        self.label_40.setMaximumSize(QSize(100, 16777215))

        self.gridLayout_3.addWidget(self.label_40, 5, 0, 1, 1)

        self.label_47 = QLabel(self.page_8)
        self.label_47.setObjectName(u"label_47")
        sizePolicy4.setHeightForWidth(self.label_47.sizePolicy().hasHeightForWidth())
        self.label_47.setSizePolicy(sizePolicy4)
        self.label_47.setMinimumSize(QSize(100, 0))
        self.label_47.setMaximumSize(QSize(100, 16777215))

        self.gridLayout_3.addWidget(self.label_47, 7, 0, 1, 1)

        self.label_grid_shot_des = QLabel(self.page_8)
        self.label_grid_shot_des.setObjectName(u"label_grid_shot_des")

        self.gridLayout_3.addWidget(self.label_grid_shot_des, 7, 1, 1, 1)


        self.verticalLayout_12.addLayout(self.gridLayout_3)

        self.stackedWidget_sub_grid.addWidget(self.page_8)
        self.page_9 = QWidget()
        self.page_9.setObjectName(u"page_9")
        self.verticalLayout_13 = QVBoxLayout(self.page_9)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label_grid_asset_type = QLabel(self.page_9)
        self.label_grid_asset_type.setObjectName(u"label_grid_asset_type")

        self.gridLayout_2.addWidget(self.label_grid_asset_type, 1, 1, 1, 1)

        self.label_21 = QLabel(self.page_9)
        self.label_21.setObjectName(u"label_21")
        sizePolicy4.setHeightForWidth(self.label_21.sizePolicy().hasHeightForWidth())
        self.label_21.setSizePolicy(sizePolicy4)
        self.label_21.setMaximumSize(QSize(100, 16777215))

        self.gridLayout_2.addWidget(self.label_21, 1, 0, 1, 1)

        self.label_grid_asset_des = QLabel(self.page_9)
        self.label_grid_asset_des.setObjectName(u"label_grid_asset_des")

        self.gridLayout_2.addWidget(self.label_grid_asset_des, 6, 1, 1, 1)

        self.label_31 = QLabel(self.page_9)
        self.label_31.setObjectName(u"label_31")
        sizePolicy4.setHeightForWidth(self.label_31.sizePolicy().hasHeightForWidth())
        self.label_31.setSizePolicy(sizePolicy4)
        self.label_31.setMaximumSize(QSize(100, 16777215))

        self.gridLayout_2.addWidget(self.label_31, 6, 0, 1, 1)

        self.label_23 = QLabel(self.page_9)
        self.label_23.setObjectName(u"label_23")
        sizePolicy4.setHeightForWidth(self.label_23.sizePolicy().hasHeightForWidth())
        self.label_23.setSizePolicy(sizePolicy4)
        self.label_23.setMaximumSize(QSize(100, 16777215))

        self.gridLayout_2.addWidget(self.label_23, 2, 0, 1, 1)

        self.label_20 = QLabel(self.page_9)
        self.label_20.setObjectName(u"label_20")
        sizePolicy4.setHeightForWidth(self.label_20.sizePolicy().hasHeightForWidth())
        self.label_20.setSizePolicy(sizePolicy4)
        self.label_20.setMaximumSize(QSize(100, 16777215))

        self.gridLayout_2.addWidget(self.label_20, 0, 0, 1, 1)

        self.label_grid_asset_date = QLabel(self.page_9)
        self.label_grid_asset_date.setObjectName(u"label_grid_asset_date")

        self.gridLayout_2.addWidget(self.label_grid_asset_date, 4, 1, 1, 1)

        self.label_grid_asset_name = QLabel(self.page_9)
        self.label_grid_asset_name.setObjectName(u"label_grid_asset_name")

        self.gridLayout_2.addWidget(self.label_grid_asset_name, 0, 1, 1, 1)

        self.label_27 = QLabel(self.page_9)
        self.label_27.setObjectName(u"label_27")
        sizePolicy4.setHeightForWidth(self.label_27.sizePolicy().hasHeightForWidth())
        self.label_27.setSizePolicy(sizePolicy4)
        self.label_27.setMaximumSize(QSize(100, 16777215))

        self.gridLayout_2.addWidget(self.label_27, 4, 0, 1, 1)

        self.label_25 = QLabel(self.page_9)
        self.label_25.setObjectName(u"label_25")
        sizePolicy4.setHeightForWidth(self.label_25.sizePolicy().hasHeightForWidth())
        self.label_25.setSizePolicy(sizePolicy4)
        self.label_25.setMaximumSize(QSize(100, 16777215))

        self.gridLayout_2.addWidget(self.label_25, 3, 0, 1, 1)

        self.label_grid_asset_artist = QLabel(self.page_9)
        self.label_grid_asset_artist.setObjectName(u"label_grid_asset_artist")

        self.gridLayout_2.addWidget(self.label_grid_asset_artist, 5, 1, 1, 1)

        self.label_grid_asset_link = QLabel(self.page_9)
        self.label_grid_asset_link.setObjectName(u"label_grid_asset_link")

        self.gridLayout_2.addWidget(self.label_grid_asset_link, 3, 1, 1, 1)

        self.label_29 = QLabel(self.page_9)
        self.label_29.setObjectName(u"label_29")
        sizePolicy4.setHeightForWidth(self.label_29.sizePolicy().hasHeightForWidth())
        self.label_29.setSizePolicy(sizePolicy4)
        self.label_29.setMaximumSize(QSize(100, 16777215))

        self.gridLayout_2.addWidget(self.label_29, 5, 0, 1, 1)

        self.label_grid_asset_ver = QLabel(self.page_9)
        self.label_grid_asset_ver.setObjectName(u"label_grid_asset_ver")

        self.gridLayout_2.addWidget(self.label_grid_asset_ver, 2, 1, 1, 1)


        self.verticalLayout_13.addLayout(self.gridLayout_2)

        self.stackedWidget_sub_grid.addWidget(self.page_9)

        self.verticalLayout_11.addWidget(self.stackedWidget_sub_grid)


        self.verticalLayout_10.addWidget(self.frame)

        self.stackedWidget_sub.addWidget(self.page_7)
        self.page_10 = QWidget()
        self.page_10.setObjectName(u"page_10")
        self.horizontalLayout_2 = QHBoxLayout(self.page_10)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.tabWidget_3 = QTabWidget(self.page_10)
        self.tabWidget_3.setObjectName(u"tabWidget_3")
        self.tab_8 = QWidget()
        self.tab_8.setObjectName(u"tab_8")
        self.verticalLayout_21 = QVBoxLayout(self.tab_8)
        self.verticalLayout_21.setObjectName(u"verticalLayout_21")
        self.pushButton_new_wip_3 = QPushButton(self.tab_8)
        self.pushButton_new_wip_3.setObjectName(u"pushButton_new_wip_3")

        self.verticalLayout_21.addWidget(self.pushButton_new_wip_3)

        self.tableWidget_list_wip = QTableWidget(self.tab_8)
        self.tableWidget_list_wip.setObjectName(u"tableWidget_list_wip")

        self.verticalLayout_21.addWidget(self.tableWidget_list_wip)

        self.tabWidget_3.addTab(self.tab_8, "")
        self.tab_9 = QWidget()
        self.tab_9.setObjectName(u"tab_9")
        self.verticalLayout_22 = QVBoxLayout(self.tab_9)
        self.verticalLayout_22.setObjectName(u"verticalLayout_22")
        self.pushButton_new_pub_3 = QPushButton(self.tab_9)
        self.pushButton_new_pub_3.setObjectName(u"pushButton_new_pub_3")

        self.verticalLayout_22.addWidget(self.pushButton_new_pub_3)

        self.tableWidget_list_pub = QTableWidget(self.tab_9)
        self.tableWidget_list_pub.setObjectName(u"tableWidget_list_pub")

        self.verticalLayout_22.addWidget(self.tableWidget_list_pub)

        self.tabWidget_3.addTab(self.tab_9, "")

        self.horizontalLayout_2.addWidget(self.tabWidget_3)

        self.stackedWidget_sub_list = QStackedWidget(self.page_10)
        self.stackedWidget_sub_list.setObjectName(u"stackedWidget_sub_list")
        self.page_12 = QWidget()
        self.page_12.setObjectName(u"page_12")
        self.verticalLayout_15 = QVBoxLayout(self.page_12)
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.label_list_shot_thumbnail = QLabel(self.page_12)
        self.label_list_shot_thumbnail.setObjectName(u"label_list_shot_thumbnail")
        sizePolicy.setHeightForWidth(self.label_list_shot_thumbnail.sizePolicy().hasHeightForWidth())
        self.label_list_shot_thumbnail.setSizePolicy(sizePolicy)
        self.label_list_shot_thumbnail.setMinimumSize(QSize(0, 200))
        self.label_list_shot_thumbnail.setMaximumSize(QSize(16777215, 200))

        self.verticalLayout_15.addWidget(self.label_list_shot_thumbnail)

        self.gridLayout_5 = QGridLayout()
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.label_list_shot_name = QLabel(self.page_12)
        self.label_list_shot_name.setObjectName(u"label_list_shot_name")

        self.gridLayout_5.addWidget(self.label_list_shot_name, 0, 1, 1, 1)

        self.label_75 = QLabel(self.page_12)
        self.label_75.setObjectName(u"label_75")

        self.gridLayout_5.addWidget(self.label_75, 5, 0, 1, 1)

        self.label_list_shot_type = QLabel(self.page_12)
        self.label_list_shot_type.setObjectName(u"label_list_shot_type")

        self.gridLayout_5.addWidget(self.label_list_shot_type, 1, 1, 1, 1)

        self.label_67 = QLabel(self.page_12)
        self.label_67.setObjectName(u"label_67")

        self.gridLayout_5.addWidget(self.label_67, 1, 0, 1, 1)

        self.label_69 = QLabel(self.page_12)
        self.label_69.setObjectName(u"label_69")

        self.gridLayout_5.addWidget(self.label_69, 2, 0, 1, 1)

        self.label_list_shot_link = QLabel(self.page_12)
        self.label_list_shot_link.setObjectName(u"label_list_shot_link")

        self.gridLayout_5.addWidget(self.label_list_shot_link, 3, 1, 1, 1)

        self.label_list_shot_frame = QLabel(self.page_12)
        self.label_list_shot_frame.setObjectName(u"label_list_shot_frame")

        self.gridLayout_5.addWidget(self.label_list_shot_frame, 6, 1, 1, 1)

        self.label_list_shot_artist = QLabel(self.page_12)
        self.label_list_shot_artist.setObjectName(u"label_list_shot_artist")

        self.gridLayout_5.addWidget(self.label_list_shot_artist, 5, 1, 1, 1)

        self.label_77 = QLabel(self.page_12)
        self.label_77.setObjectName(u"label_77")

        self.gridLayout_5.addWidget(self.label_77, 6, 0, 1, 1)

        self.label_71 = QLabel(self.page_12)
        self.label_71.setObjectName(u"label_71")

        self.gridLayout_5.addWidget(self.label_71, 3, 0, 1, 1)

        self.label_65 = QLabel(self.page_12)
        self.label_65.setObjectName(u"label_65")

        self.gridLayout_5.addWidget(self.label_65, 0, 0, 1, 1)

        self.label_list_shot_date = QLabel(self.page_12)
        self.label_list_shot_date.setObjectName(u"label_list_shot_date")

        self.gridLayout_5.addWidget(self.label_list_shot_date, 4, 1, 1, 1)

        self.label_list_shot_ver = QLabel(self.page_12)
        self.label_list_shot_ver.setObjectName(u"label_list_shot_ver")

        self.gridLayout_5.addWidget(self.label_list_shot_ver, 2, 1, 1, 1)

        self.label_73 = QLabel(self.page_12)
        self.label_73.setObjectName(u"label_73")

        self.gridLayout_5.addWidget(self.label_73, 4, 0, 1, 1)

        self.label_79 = QLabel(self.page_12)
        self.label_79.setObjectName(u"label_79")

        self.gridLayout_5.addWidget(self.label_79, 7, 0, 1, 1)

        self.label_list_shot_des = QLabel(self.page_12)
        self.label_list_shot_des.setObjectName(u"label_list_shot_des")

        self.gridLayout_5.addWidget(self.label_list_shot_des, 7, 1, 1, 1)


        self.verticalLayout_15.addLayout(self.gridLayout_5)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_15.addItem(self.verticalSpacer_2)

        self.stackedWidget_sub_list.addWidget(self.page_12)
        self.page_11 = QWidget()
        self.page_11.setObjectName(u"page_11")
        self.verticalLayout_14 = QVBoxLayout(self.page_11)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.label_list_asset_thumbnail = QLabel(self.page_11)
        self.label_list_asset_thumbnail.setObjectName(u"label_list_asset_thumbnail")
        sizePolicy.setHeightForWidth(self.label_list_asset_thumbnail.sizePolicy().hasHeightForWidth())
        self.label_list_asset_thumbnail.setSizePolicy(sizePolicy)
        self.label_list_asset_thumbnail.setMinimumSize(QSize(0, 200))
        self.label_list_asset_thumbnail.setMaximumSize(QSize(16777215, 200))

        self.verticalLayout_14.addWidget(self.label_list_asset_thumbnail)

        self.gridLayout_4 = QGridLayout()
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.label_list_asset_name = QLabel(self.page_11)
        self.label_list_asset_name.setObjectName(u"label_list_asset_name")

        self.gridLayout_4.addWidget(self.label_list_asset_name, 0, 1, 1, 1)

        self.label_56 = QLabel(self.page_11)
        self.label_56.setObjectName(u"label_56")

        self.gridLayout_4.addWidget(self.label_56, 3, 0, 1, 1)

        self.label_58 = QLabel(self.page_11)
        self.label_58.setObjectName(u"label_58")

        self.gridLayout_4.addWidget(self.label_58, 4, 0, 1, 1)

        self.label_list_asset_ver = QLabel(self.page_11)
        self.label_list_asset_ver.setObjectName(u"label_list_asset_ver")

        self.gridLayout_4.addWidget(self.label_list_asset_ver, 2, 1, 1, 1)

        self.label_50 = QLabel(self.page_11)
        self.label_50.setObjectName(u"label_50")

        self.gridLayout_4.addWidget(self.label_50, 0, 0, 1, 1)

        self.label_52 = QLabel(self.page_11)
        self.label_52.setObjectName(u"label_52")

        self.gridLayout_4.addWidget(self.label_52, 1, 0, 1, 1)

        self.label_list_asset_type = QLabel(self.page_11)
        self.label_list_asset_type.setObjectName(u"label_list_asset_type")

        self.gridLayout_4.addWidget(self.label_list_asset_type, 1, 1, 1, 1)

        self.label_list_asset_date = QLabel(self.page_11)
        self.label_list_asset_date.setObjectName(u"label_list_asset_date")

        self.gridLayout_4.addWidget(self.label_list_asset_date, 4, 1, 1, 1)

        self.label_list_asset_link = QLabel(self.page_11)
        self.label_list_asset_link.setObjectName(u"label_list_asset_link")

        self.gridLayout_4.addWidget(self.label_list_asset_link, 3, 1, 1, 1)

        self.label_60 = QLabel(self.page_11)
        self.label_60.setObjectName(u"label_60")

        self.gridLayout_4.addWidget(self.label_60, 5, 0, 1, 1)

        self.label_list_asset_artist = QLabel(self.page_11)
        self.label_list_asset_artist.setObjectName(u"label_list_asset_artist")

        self.gridLayout_4.addWidget(self.label_list_asset_artist, 5, 1, 1, 1)

        self.label_list_asset_des = QLabel(self.page_11)
        self.label_list_asset_des.setObjectName(u"label_list_asset_des")

        self.gridLayout_4.addWidget(self.label_list_asset_des, 6, 1, 1, 1)

        self.label_53 = QLabel(self.page_11)
        self.label_53.setObjectName(u"label_53")

        self.gridLayout_4.addWidget(self.label_53, 2, 0, 1, 1)

        self.label_62 = QLabel(self.page_11)
        self.label_62.setObjectName(u"label_62")

        self.gridLayout_4.addWidget(self.label_62, 6, 0, 1, 1)


        self.verticalLayout_14.addLayout(self.gridLayout_4)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_14.addItem(self.verticalSpacer)

        self.stackedWidget_sub_list.addWidget(self.page_11)

        self.horizontalLayout_2.addWidget(self.stackedWidget_sub_list)

        self.stackedWidget_sub.addWidget(self.page_10)

        self.gridLayout.addWidget(self.stackedWidget_sub, 1, 1, 1, 1)


        self.verticalLayout_4.addLayout(self.gridLayout)

        self.stackedWidget_main.addWidget(self.page_2)

        self.verticalLayout.addWidget(self.stackedWidget_main)


        self.retranslateUi(Form)

        self.stackedWidget_main.setCurrentIndex(1)
        self.stackedWidget_path.setCurrentIndex(1)
        self.tabWidget.setCurrentIndex(0)
        self.stackedWidget_sub.setCurrentIndex(1)
        self.tabWidget_grid_full_wip.setCurrentIndex(0)
        self.tabWidget_2.setCurrentIndex(1)
        self.stackedWidget_sub_grid.setCurrentIndex(0)
        self.tabWidget_3.setCurrentIndex(0)
        self.stackedWidget_sub_list.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label.setText(QCoreApplication.translate("Form", u"Loader", None))
        self.label_username.setText(QCoreApplication.translate("Form", u"User Name", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"Project", None))
        self.label_asset.setText(QCoreApplication.translate("Form", u"Assets", None))
        self.label_10.setText(QCoreApplication.translate("Form", u"\u25b6", None))
        self.label_env.setText(QCoreApplication.translate("Form", u"Environment", None))
        self.label_8.setText(QCoreApplication.translate("Form", u"\u25b6", None))
        self.label_mod.setText(QCoreApplication.translate("Form", u"Modeling", None))
        self.label_seq.setText(QCoreApplication.translate("Form", u"Sequence", None))
        self.label_15.setText(QCoreApplication.translate("Form", u"\u25b6", None))
        self.label_shot.setText(QCoreApplication.translate("Form", u"Shot", None))
        self.label_13.setText(QCoreApplication.translate("Form", u"\u25b6", None))
        self.label_ani.setText(QCoreApplication.translate("Form", u"animation", None))
        self.pushButton_grid.setText(QCoreApplication.translate("Form", u"\uadf8\ub9ac\ub4dc", None))
        self.pushButton_list.setText(QCoreApplication.translate("Form", u"\ub9ac\uc2a4\ud2b8", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("Form", u"My Tasks", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("Form", u"Assets", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QCoreApplication.translate("Form", u"Shots", None))
        self.pushButton_home.setText(QCoreApplication.translate("Form", u"home", None))
        self.label_project_name.setText(QCoreApplication.translate("Form", u"Project Name", None))
        self.pushButton_new_wip_1.setText(QCoreApplication.translate("Form", u"Create New File", None))
        self.tabWidget_grid_full_wip.setTabText(self.tabWidget_grid_full_wip.indexOf(self.tab_4), QCoreApplication.translate("Form", u"Working", None))
        self.pushButton_new_pub_1.setText(QCoreApplication.translate("Form", u"Create New File", None))
        self.tabWidget_grid_full_wip.setTabText(self.tabWidget_grid_full_wip.indexOf(self.tab_5), QCoreApplication.translate("Form", u"Publishes", None))
        self.pushButton_new_wip_2.setText(QCoreApplication.translate("Form", u"Create New File", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_6), QCoreApplication.translate("Form", u"Working", None))
        self.pushButton_new_pub_2.setText(QCoreApplication.translate("Form", u"Create New File", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_7), QCoreApplication.translate("Form", u"Publishes", None))
        self.label_35.setText(QCoreApplication.translate("Form", u"Type", None))
        self.label_41.setText(QCoreApplication.translate("Form", u"Frame Range", None))
        self.label_grid_shot_name.setText("")
        self.label_37.setText(QCoreApplication.translate("Form", u"Version", None))
        self.label_33.setText(QCoreApplication.translate("Form", u"Name", None))
        self.label_grid_shot_ver.setText("")
        self.label_grid_shot_artist.setText("")
        self.label_grid_shot_type.setText("")
        self.label_39.setText(QCoreApplication.translate("Form", u"Date", None))
        self.label_grid_shot_date.setText("")
        self.label_grid_shot_link.setText("")
        self.label_grid_shot_frame.setText("")
        self.label_38.setText(QCoreApplication.translate("Form", u"Link", None))
        self.label_40.setText(QCoreApplication.translate("Form", u"Artist", None))
        self.label_47.setText(QCoreApplication.translate("Form", u"Description", None))
        self.label_grid_shot_des.setText("")
        self.label_grid_asset_type.setText("")
        self.label_21.setText(QCoreApplication.translate("Form", u"Type", None))
        self.label_grid_asset_des.setText("")
        self.label_31.setText(QCoreApplication.translate("Form", u"Description", None))
        self.label_23.setText(QCoreApplication.translate("Form", u"Version", None))
        self.label_20.setText(QCoreApplication.translate("Form", u"Name", None))
        self.label_grid_asset_date.setText("")
        self.label_grid_asset_name.setText("")
        self.label_27.setText(QCoreApplication.translate("Form", u"Date", None))
        self.label_25.setText(QCoreApplication.translate("Form", u"Link", None))
        self.label_grid_asset_artist.setText("")
        self.label_grid_asset_link.setText("")
        self.label_29.setText(QCoreApplication.translate("Form", u"Artist", None))
        self.label_grid_asset_ver.setText("")
        self.pushButton_new_wip_3.setText(QCoreApplication.translate("Form", u"Create New File", None))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.tab_8), QCoreApplication.translate("Form", u"Working", None))
        self.pushButton_new_pub_3.setText(QCoreApplication.translate("Form", u"Create New File", None))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.tab_9), QCoreApplication.translate("Form", u"Publishes", None))
        self.label_list_shot_thumbnail.setText(QCoreApplication.translate("Form", u"TextLabel", None))
        self.label_list_shot_name.setText("")
        self.label_75.setText(QCoreApplication.translate("Form", u"Artist", None))
        self.label_list_shot_type.setText("")
        self.label_67.setText(QCoreApplication.translate("Form", u"Type", None))
        self.label_69.setText(QCoreApplication.translate("Form", u"Version", None))
        self.label_list_shot_link.setText("")
        self.label_list_shot_frame.setText("")
        self.label_list_shot_artist.setText("")
        self.label_77.setText(QCoreApplication.translate("Form", u"Frame Range", None))
        self.label_71.setText(QCoreApplication.translate("Form", u"Link", None))
        self.label_65.setText(QCoreApplication.translate("Form", u"Name", None))
        self.label_list_shot_date.setText("")
        self.label_list_shot_ver.setText("")
        self.label_73.setText(QCoreApplication.translate("Form", u"Date", None))
        self.label_79.setText(QCoreApplication.translate("Form", u"Description", None))
        self.label_list_shot_des.setText("")
        self.label_list_asset_thumbnail.setText(QCoreApplication.translate("Form", u"TextLabel", None))
        self.label_list_asset_name.setText("")
        self.label_56.setText(QCoreApplication.translate("Form", u"Link", None))
        self.label_58.setText(QCoreApplication.translate("Form", u"Date", None))
        self.label_list_asset_ver.setText("")
        self.label_50.setText(QCoreApplication.translate("Form", u"Name", None))
        self.label_52.setText(QCoreApplication.translate("Form", u"Type", None))
        self.label_list_asset_type.setText("")
        self.label_list_asset_date.setText("")
        self.label_list_asset_link.setText("")
        self.label_60.setText(QCoreApplication.translate("Form", u"Artist", None))
        self.label_list_asset_artist.setText("")
        self.label_list_asset_des.setText("")
        self.label_53.setText(QCoreApplication.translate("Form", u"Version", None))
        self.label_62.setText(QCoreApplication.translate("Form", u"Description", None))
    # retranslateUi

