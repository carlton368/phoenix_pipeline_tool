# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'publishercMzskL.ui'
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
    QHeaderView, QLabel, QPlainTextEdit, QPushButton,
    QSizePolicy, QSpacerItem, QTextEdit, QTreeWidget,
    QTreeWidgetItem, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(964, 721)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(15, 15, 15, 15)
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

        self.verticalLayout_16 = QVBoxLayout()
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.label_username = QLabel(Form)
        self.label_username.setObjectName(u"label_username")

        self.verticalLayout_16.addWidget(self.label_username, 0, Qt.AlignRight)

        self.label_project_name = QLabel(Form)
        self.label_project_name.setObjectName(u"label_project_name")

        self.verticalLayout_16.addWidget(self.label_project_name, 0, Qt.AlignRight)


        self.horizontalLayout.addLayout(self.verticalLayout_16)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.treeWidget_main = QTreeWidget(Form)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"1");
        self.treeWidget_main.setHeaderItem(__qtreewidgetitem)
        self.treeWidget_main.setObjectName(u"treeWidget_main")
        self.treeWidget_main.setMinimumSize(QSize(500, 600))
        self.treeWidget_main.header().setVisible(False)

        self.horizontalLayout_2.addWidget(self.treeWidget_main)

        self.horizontalSpacer = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(-1, -1, 0, -1)
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(-1, -1, 0, -1)
        self.label_icon = QLabel(Form)
        self.label_icon.setObjectName(u"label_icon")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_icon.sizePolicy().hasHeightForWidth())
        self.label_icon.setSizePolicy(sizePolicy)
        self.label_icon.setMinimumSize(QSize(80, 80))
        self.label_icon.setMaximumSize(QSize(80, 80))
        self.label_icon.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_3.addWidget(self.label_icon)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.label_file_name = QLabel(Form)
        self.label_file_name.setObjectName(u"label_file_name")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_file_name.sizePolicy().hasHeightForWidth())
        self.label_file_name.setSizePolicy(sizePolicy1)
        self.label_file_name.setMaximumSize(QSize(16777215, 35))
        font1 = QFont()
        font1.setPointSize(19)
        self.label_file_name.setFont(font1)

        self.verticalLayout_4.addWidget(self.label_file_name)

        self.label_file_type = QLabel(Form)
        self.label_file_type.setObjectName(u"label_file_type")
        self.label_file_type.setEnabled(True)
        sizePolicy1.setHeightForWidth(self.label_file_type.sizePolicy().hasHeightForWidth())
        self.label_file_type.setSizePolicy(sizePolicy1)
        self.label_file_type.setMaximumSize(QSize(16777215, 30))

        self.verticalLayout_4.addWidget(self.label_file_type)


        self.horizontalLayout_3.addLayout(self.verticalLayout_4)


        self.verticalLayout_3.addLayout(self.horizontalLayout_3)

        self.verticalSpacer_4 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_3.addItem(self.verticalSpacer_4)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_8 = QLabel(Form)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout.addWidget(self.label_8, 0, 0, 1, 1, Qt.AlignBottom)

        self.frame_2 = QFrame(Form)
        self.frame_2.setObjectName(u"frame_2")
        sizePolicy.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy)
        self.frame_2.setMinimumSize(QSize(200, 100))
        self.frame_2.setMaximumSize(QSize(200, 100))
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.verticalLayout_6 = QVBoxLayout(self.frame_2)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.label_thum_img = QLabel(self.frame_2)
        self.label_thum_img.setObjectName(u"label_thum_img")

        self.verticalLayout_6.addWidget(self.label_thum_img)


        self.gridLayout.addWidget(self.frame_2, 1, 1, 1, 1)

        self.label_9 = QLabel(Form)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout.addWidget(self.label_9, 0, 1, 1, 1, Qt.AlignBottom)

        self.description = QTextEdit(Form)
        self.description.setObjectName(u"description")
        self.description.setMinimumSize(QSize(200, 100))
        self.description.setMaximumSize(QSize(200, 100))

        self.gridLayout.addWidget(self.description, 1, 0, 1, 1)


        self.verticalLayout_3.addLayout(self.gridLayout)

        self.verticalSpacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_3.addItem(self.verticalSpacer)

        self.label_13 = QLabel(Form)
        self.label_13.setObjectName(u"label_13")
        font2 = QFont()
        font2.setPointSize(15)
        self.label_13.setFont(font2)

        self.verticalLayout_3.addWidget(self.label_13)

        self.label_summary_context = QLabel(Form)
        self.label_summary_context.setObjectName(u"label_summary_context")

        self.verticalLayout_3.addWidget(self.label_summary_context)

        self.verticalSpacer_3 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_3.addItem(self.verticalSpacer_3)

        self.label_file_name2 = QLabel(Form)
        self.label_file_name2.setObjectName(u"label_file_name2")
        font3 = QFont()
        font3.setBold(True)
        self.label_file_name2.setFont(font3)

        self.verticalLayout_3.addWidget(self.label_file_name2)

        self.label_file_name_context = QLabel(Form)
        self.label_file_name_context.setObjectName(u"label_file_name_context")

        self.verticalLayout_3.addWidget(self.label_file_name_context)

        self.verticalSpacer_5 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_3.addItem(self.verticalSpacer_5)

        self.plainTextEdit_validation_report = QPlainTextEdit(Form)
        self.plainTextEdit_validation_report.setObjectName(u"plainTextEdit_validation_report")
        self.plainTextEdit_validation_report.setFrameShape(QFrame.NoFrame)
        self.plainTextEdit_validation_report.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.plainTextEdit_validation_report.setReadOnly(True)

        self.verticalLayout_3.addWidget(self.plainTextEdit_validation_report)


        self.horizontalLayout_2.addLayout(self.verticalLayout_3)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_19 = QHBoxLayout()
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.horizontalLayout_19.setContentsMargins(-1, -1, -1, 0)
        self.label_validation_error = QLabel(Form)
        self.label_validation_error.setObjectName(u"label_validation_error")
        sizePolicy.setHeightForWidth(self.label_validation_error.sizePolicy().hasHeightForWidth())
        self.label_validation_error.setSizePolicy(sizePolicy)
        self.label_validation_error.setBaseSize(QSize(40, 10))
        self.label_validation_error.setTextInteractionFlags(Qt.NoTextInteraction)

        self.horizontalLayout_19.addWidget(self.label_validation_error)

        self.pushButton_validate = QPushButton(Form)
        self.pushButton_validate.setObjectName(u"pushButton_validate")

        self.horizontalLayout_19.addWidget(self.pushButton_validate)

        self.pushButton_publish = QPushButton(Form)
        self.pushButton_publish.setObjectName(u"pushButton_publish")

        self.horizontalLayout_19.addWidget(self.pushButton_publish)


        self.verticalLayout.addLayout(self.horizontalLayout_19)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label.setText(QCoreApplication.translate("Form", u"Publish", None))
        self.label_username.setText(QCoreApplication.translate("Form", u"User Name", None))
        self.label_project_name.setText(QCoreApplication.translate("Form", u"Project Name", None))
        self.label_icon.setText(QCoreApplication.translate("Form", u"Icon", None))
        self.label_file_name.setText(QCoreApplication.translate("Form", u"scene_v002.ma", None))
        self.label_file_type.setText(QCoreApplication.translate("Form", u"Maya Session", None))
        self.label_8.setText(QCoreApplication.translate("Form", u"Desciption", None))
        self.label_thum_img.setText("")
        self.label_9.setText(QCoreApplication.translate("Form", u"Thumbnail", None))
        self.label_13.setText(QCoreApplication.translate("Form", u"Summary :", None))
        self.label_summary_context.setText(QCoreApplication.translate("Form", u"The following items will be processed:", None))
        self.label_file_name2.setText(QCoreApplication.translate("Form", u"TextLabel", None))
        self.label_file_name_context.setText(QCoreApplication.translate("Form", u"- Publish to Flow Production Tracking", None))
        self.label_validation_error.setText("")
        self.pushButton_validate.setText(QCoreApplication.translate("Form", u"Validate", None))
        self.pushButton_publish.setText(QCoreApplication.translate("Form", u"Publish", None))
    # retranslateUi

