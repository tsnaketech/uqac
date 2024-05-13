#!/usr/bin/python3
# -*- coding: utf-8 -*-

###### Import ########

import json
import os
import re
import webbrowser

from PySide2 import QtWidgets, QtGui, QtCore

from package.pathfinder import MongoDB

###### Variable ######


###### Function ######

class MainWindows(QtWidgets.QWidget):
    def __init__(self, ctx):
        super().__init__()
        self.ctx = ctx
        self.setWindowTitle("PyPathfinder")
        self.setup_ui()
        self.server_information_read()
        self.initJson()

    def setup_ui(self):
        self.create_widgets()
        self.modify_widgets()
        self.create_layouts()
        self.add_layouts_to_layouts()
        self.add_widgets_to_layouts()
        self.setup_connections()

    def create_widgets(self):
        # Search
        self.le_search = QtWidgets.QLineEdit()
        self.l_search = QtWidgets.QLabel("Search :")

        # Composents
        self.l_composents = QtWidgets.QLabel("Composants :")
        self.cb_composentsV = QtWidgets.QCheckBox("Verbal (V)")
        self.cb_composentsS = QtWidgets.QCheckBox("Somatic (S)")
        self.cb_composentsM = QtWidgets.QCheckBox("Material (M)")

        # Level
        self.l_level = QtWidgets.QLabel("Level :")
        self.l_min = QtWidgets.QLabel("Min :")
        self.l_max = QtWidgets.QLabel("Max :")
        self.sb_levelmin = QtWidgets.QSpinBox(maximum=9)
        self.sb_levelmax = QtWidgets.QSpinBox(maximum=9)

        # Classes
        self.l_classes= QtWidgets.QLabel("Classes :")
        self.cb_classAdept = QtWidgets.QCheckBox("Adept", self)
        self.cb_classAlchemist = QtWidgets.QCheckBox("Alchemist", self)
        self.cb_classAntipaladin = QtWidgets.QCheckBox("Antipaladin", self)
        self.cb_classBard = QtWidgets.QCheckBox("Bard", self)
        self.cb_classBloodrager = QtWidgets.QCheckBox("Bloodrager", self)
        self.cb_classCleric = QtWidgets.QCheckBox("Cleric", self)
        self.cb_classDruid = QtWidgets.QCheckBox("Druid", self)
        self.cb_classInquisitor = QtWidgets.QCheckBox("Inquisitor", self)
        self.cb_classMagus = QtWidgets.QCheckBox("Magus", self)
        self.cb_classOracle = QtWidgets.QCheckBox("Oracle", self)
        self.cb_classPaladin = QtWidgets.QCheckBox("Paladin", self)
        self.cb_classRanger = QtWidgets.QCheckBox("Ranger", self)
        self.cb_classShaman = QtWidgets.QCheckBox("Shaman", self)
        self.cb_classSorcerer = QtWidgets.QCheckBox("Sorcerer", self)
        self.cb_classSummoner = QtWidgets.QCheckBox("Summoner", self)
        self.cb_classWitch = QtWidgets.QCheckBox("Witch", self)
        self.cb_classWizard = QtWidgets.QCheckBox("Wizard", self)

        # Description
        self.le_description = QtWidgets.QLineEdit()
        self.l_description = QtWidgets.QLabel("Description :")

        # Bouton for search
        self.btn_search = QtWidgets.QPushButton("Search spells")

        # Bouton for spark
        self.btn_spark = QtWidgets.QPushButton("Information MongoDB")

        # Display spells
        self.lw_spells = QtWidgets.QListWidget()
        self.tw_spells = QtWidgets.QTableWidget()

        # List
        self.list_classes = [self.cb_classAdept, self.cb_classAlchemist, self.cb_classAntipaladin, self.cb_classBard, self.cb_classBloodrager,self.cb_classCleric, self.cb_classDruid, self.cb_classInquisitor, self.cb_classMagus, self.cb_classOracle, self.cb_classPaladin, self.cb_classRanger, self.cb_classShaman, self.cb_classSorcerer, self.cb_classSummoner, self.cb_classWitch, self.cb_classWizard]
        self.list_name = ["Adept", "Alchemist", "Antipaladin", "Bard", "Bloodrager", "Cleric", "Druid", "Inquisitor", "Magus", "Oracle", "Paladin", "Ranger", "Shaman", "Sorcerer", "Summoner", "Witch", "Wizard"]
        self.list_composants = [self.cb_composentsV,self.cb_composentsS,self.cb_composentsM]
        self.list_level = [self.sb_levelmin,self.sb_levelmax]

    def modify_widgets(self):
        self.l_search.setBuddy(self.le_search)
        self.sb_levelmax.setValue(9)
        self.l_description.setBuddy(self.le_description)
        css_file = self.ctx.get_resource("style.css")
        with open(css_file, "r") as f:
            self.setStyleSheet(f.read())

    def create_layouts(self):
        # For application
        self.main_layout = QtWidgets.QGridLayout(self)
        self.search_layout = QtWidgets.QFormLayout()
        self.descrpiption_layout = QtWidgets.QFormLayout()
        self.composents_layout = QtWidgets.QFormLayout()
        self.level_layout = QtWidgets.QFormLayout()
        self.levelcompo_layout = QtWidgets.QHBoxLayout()
        self.classes_layout = QtWidgets.QFormLayout()

    def add_layouts_to_layouts(self):
        self.levelcompo_layout.addLayout(self.composents_layout)
        self.levelcompo_layout.addLayout(self.level_layout)
        self.main_layout.addLayout(self.search_layout, 0, 0)
        self.main_layout.addLayout(self.levelcompo_layout, 2, 0)
        self.main_layout.addLayout(self.classes_layout, 4, 0)
        self.main_layout.addLayout(self.descrpiption_layout, 6, 0)

    def add_widgets_to_layouts(self):
        self.search_layout.addRow(self.l_search)
        self.search_layout.addRow(self.le_search)
        self.composents_layout.addRow(self.l_composents)
        for composents in self.list_composants:
            self.composents_layout.addRow(composents)
        self.level_layout.addWidget(self.l_level)
        for level in self.list_level:
            self.level_layout.addRow(level)
        self.classes_layout.addRow(self.l_classes)
        for box in range(0, int(len(self.list_classes)), 2):
            try:
                self.classes_layout.addRow(self.list_classes[box],self.list_classes[box+1])
            except:
                self.classes_layout.addRow(self.list_classes[box])
        self.descrpiption_layout.addRow(self.l_description)
        self.descrpiption_layout.addRow(self.le_description)
        self.main_layout.addWidget(self.lw_spells, 0, 1, 10, 1)
        self.main_layout.addWidget(self.btn_spark, 8, 0, 1, 1)
        self.main_layout.addWidget(self.btn_search, 9, 0,1,1)
        #self.main_layout.addWidget(self.sb, 0, 2, 9, 1)

    def setup_connections(self):
        self.btn_spark.clicked.connect(self.information)
        self.btn_search.clicked.connect(self.search_spells)
        self.sb_levelmin.valueChanged.connect(self.check_level)
        self.sb_levelmax.valueChanged.connect(self.check_level)
        self.lw_spells.itemDoubleClicked.connect(self.open_url)
        self.lw_spells.itemSelectionChanged.connect(self.info_spell)
        #self.test()

    # Other function

    def add_spells_to_listwidget(self, spell):
        lw_spell = QtWidgets.QListWidgetItem(spell)
        icon = QtGui.QIcon(self.icons(spell))
        icon.actualSize(QtCore.QSize(32, 32))
        lw_spell.setIcon(icon)
        #lw_spells.setSizeHint(QtCore.QSize(64, 64))
        self.lw_spells.addItem(lw_spell)

    def check_empty(self):
        if self.result:
            pass

    def check_level(self):
        if self.sb_levelmin.value() >= self.sb_levelmax.value():
            self.sb_levelmin.setValue(self.sb_levelmax.value())
        if self.sb_levelmax.value() <= self.sb_levelmin.value():
            self.sb_levelmax.setValue(self.sb_levelmin.value())

    def clear(self):
        self.search = self.le_search.clear()
        self.composents = [composent.setChecked(0) for composent in self.list_composants]
        self.list_level[0].setValue(0)
        self.list_level[1].setValue(9)
        self.classes = [classe.setChecked(0) for classe in self.list_classes]
        self.descrpiption = self.le_description.clear()

    def icons(self, name):
        file = name.split('(')[0].strip().lower().replace("'", "_")
        try:
            icon = self.ctx.get_resource(f"img/{file}.ico")
        except:
            icon = self.ctx.get_resource(f"img/Icon.ico")
        return icon

    def info_spell(self):
        headers = ["Name","Components","Level","Classes","Description","Monters"]
        for i in range(len(headers)):
            headers[i] = "{0:13}:".format(headers[i])
        name = self.lw_spells.selectedItems()[0].text().split('(')[0].strip()
        result = [i for i in self.result if i['name'] == name]
        description = result[0]['description'].split(" ")
        [description.insert(i, "\n") for i in range(20, len(description), 20)]
        description = " ".join(description)
        monsters = self.search_monsters(name)
        values = [name, ', '.join(result[0]['components']), str(result[0]['level']), ', '.join(result[0]['classes']), description, monsters]
        dialog = QtWidgets.QDialog()
        btn_ok = QtWidgets.QPushButton("Ok")

        spell_layout = QtWidgets.QFormLayout()

        dialog.setWindowTitle(self.lw_spells.selectedItems()[0].text())

        for header, value in zip(headers, values):
            spell_layout.addRow(QtWidgets.QLabel(header), QtWidgets.QLabel(value))

        spell_layout.addWidget(btn_ok)
        btn_ok.clicked.connect(dialog.close)
        dialog.setLayout(spell_layout)
        dialog.resize(550, 300)
        dialog.exec_()

    def information(self):
        dialog = QtWidgets.QDialog()
        le_server = QtWidgets.QLineEdit(self.server)
        le_port = QtWidgets.QLineEdit(self.port)
        btn_ok = QtWidgets.QPushButton("Ok")
        spark_layout = QtWidgets.QFormLayout()
        spark_layout.addRow(QtWidgets.QLabel("Server : "), le_server)
        spark_layout.addRow(QtWidgets.QLabel("Port : "), le_port)
        spark_layout.addRow(btn_ok)
        btn_ok.clicked.connect(dialog.close)
        dialog.setLayout(spark_layout)
        dialog.resize(200, 100)
        dialog.exec_()
        self.server = le_server.text()
        self.port = le_port.text()
        self.server_information_write()

    def initJson(self):
        jsonSpells = self.ctx.get_resource("json/spells.json")
        jsonMonsters = self.ctx.get_resource("json/monsters.json")
        jsonInverse = self.ctx.get_resource("json/indexInverse.json")

        with open(jsonSpells, 'r') as f:
            self.Spells = json.load(f)

        with open(jsonMonsters, 'r') as f:
            self.Monsters = json.load(f)

        with open(jsonInverse, 'r') as f:
            self.Inverse = json.load(f)

    def print_spells(self):
        [self.add_spells_to_listwidget(f"{r['name']} (level : {r['level']})") for r in self.result]

    def open_url(self, new=2):
        name = self.lw_spells.selectedItems()[0].text().split('(')[0].strip()
        result = [i for i in self.result if i['name'] == name]
        webbrowser.open(result[0]['url'], new)

    def recovery(self):
        self.search = self.le_search.text()
        self.composents = [re.search("[A-Z]",composent.text()).group(0) for composent in self.list_composants if composent.isChecked() == True]
        self.level = [lvl.value() for lvl in self.list_level]
        self.classes = [classe.text() for classe in self.list_classes if classe.isChecked() == True]
        self.descrpiption = self.le_description.text()
        self.list_search = [self.search, self.composents, self.level, self.classes, self.descrpiption]

    def search_base(self):
        self.initJson()
        self.mc = MongoDB(server=self.server, port=self.port)
        self.mc.initJson(self.Spells)
        self.result = self.mc.query(self.list_search)
        self.mc.col.drop()
        self.mc.client.close()

    def search_monsters(self, name):
        mm = MongoDB(server=self.server, port=self.port, collection='Inverse')
        mm.initJson(self.Inverse)
        result = mm.query_monsters(name)
        mm.col.drop()
        mm.client.close()
        if result:
            [result['monsters'].insert(i, "\n") for i in range(10, len(result['monsters']), 10)]
            return ', '.join(result['monsters'])
        else:
            return 'Aucun'

    def search_spells(self):
        self.lw_spells.clear()
        self.recovery()
        self.search_base()
        self.check_empty()
        self.print_spells()
        #self.clear()

    def server_information_read(self):
        self.server_json = self.ctx.get_resource("json/server.json")
        with open(self.server_json, 'r') as f:
            info = json.load(f)
        self.server = info['server']
        self.port = info['port']

    def server_information_write(self):
        info = {}
        info['server'] = self.server
        info['port'] = self.port
        with open(self.server_json, 'w') as f:
            json.dump(info, f)

###### Program #######