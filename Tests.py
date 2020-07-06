import unittest
from Repositories import PlayTable
from Services import ServiceGame
from Entities import ButtonForRepo
import copy

class Tests(unittest.TestCase):
    def test_InitializeTable_ValidInput_TableInitilizedCorectly(self):
        player_table = PlayTable()
        AI_table = PlayTable()
        service = ServiceGame(player_table,AI_table)
        service.InitializeTable("ui", "grey", "NAI")
        table = service.GetPlayerTable()
        correct_table = []
        for i in range(8):
            row = []
            for j in range(8):
                cell = ButtonForRepo("0",i,j,"grey","NAI")
                row.append(cell)
            correct_table.append(row)
        self.assertEqual(table, correct_table)
         
    def test_AddPlayerPlane_ValidInput_PlaneAddedOnTheTable(self):
        player_table = PlayTable()
        AI_table = PlayTable()
        service = ServiceGame(player_table,AI_table)
        service.InitializeTable("ui", "grey", "NAI")
        service.AddPlayerPlane(3, 0, "ui", "blue", "NAI")
        correct_table = []
        for i in range(8):
            row = []
            for j in range(8):
                if (i == 1 and j == 1) or ((i == 2 and j == 1) or (i == 2 and j == 3)) or (i == 3 and ( j == 1 or j == 2 or j == 3)) or ((i == 4 and j == 1) or (i == 4 and j == 3)) or (i == 5 and j == 1):
                    cell = ButtonForRepo("1",i,j,"blue","NAI")
                elif i == 3 and j == 0:
                    cell = ButtonForRepo("1",i,j,"pink","NAI")
                else:
                    cell = ButtonForRepo("0",i,j,"grey","NAI")
                row.append(cell)
            correct_table.append(row)
        table = service.GetPlayerTable()
        self.assertEqual(table, correct_table)
    
    def test_AddAiPlane_ValidInput_PlaneAddedOnTheTable(self):
        player_table = PlayTable()
        AI_table = PlayTable()
        service = ServiceGame(player_table,AI_table)
        service.InitializeTable("ui", "white", "AI")
        service.AddAiPlane(3, 0, "ui")
        correct_table = []
        for i in range(8):
            row = []
            for j in range(8):
                if (i == 1 and j == 1) or ((i == 2 and j == 1) or (i == 2 and j == 3)) or (i == 3 and ( j == 1 or j == 2 or j == 3)) or ((i == 4 and j == 1) or (i == 4 and j == 3)) or (i == 5 and j == 1):
                    cell = ButtonForRepo("1",i,j,"blue","AI")
                elif i == 3 and j == 0:
                    cell = ButtonForRepo("1",i,j,"pink","AI")
                else:
                    cell = ButtonForRepo("0",i,j,"white","AI")
                row.append(cell)
            correct_table.append(row)
        table = service.GetAiTable()
        self.assertEqual(table, correct_table)
    
    def test_Reset_ValidInput_TablesReseted(self):
        player_table = PlayTable()
        AI_table = PlayTable()
        service = ServiceGame(player_table,AI_table)
        service.InitializeTable("ui", "grey", "NAI")
        service.AddPlayerPlane(3, 0, "ui", "blue", "NAI")
        table = service.GetPlayerTable()
        copy_of_table = copy.deepcopy(table)
        service.Reset("ui")
        table_after_reset = service.GetPlayerTable()
        self.assertNotEqual(copy_of_table, table_after_reset)
    
    def test_HitAi_RandomPartOfPlaneHit_CellTypeChangedToX(self):
        player_table = PlayTable()
        AI_table = PlayTable()
        service = ServiceGame(player_table,AI_table)
        service.InitializeTable("ui", "white", "AI")
        service.InitializeTable("ui","grey","NAI")
        service.AddAiPlane(3, 0, "ui")
        service.HitAi(1, 1)
        
        correct_table = []
        for i in range(8):
            row = []
            for j in range(8):
                if ((i == 2 and j == 1) or (i == 2 and j == 3)) or (i == 3 and ( j == 1 or j == 2 or j == 3)) or ((i == 4 and j == 1) or (i == 4 and j == 3)) or (i == 5 and j == 1):
                    cell = ButtonForRepo("1",i,j,"blue","AI")
                elif i == 1 and j == 1:
                    cell = ButtonForRepo("X",i,j,"X","AI")
                elif i == 3 and j == 0:
                    cell = ButtonForRepo("1",i,j,"pink","AI")
                else:
                    cell = ButtonForRepo("0",i,j,"white","AI")
                row.append(cell)
            correct_table.append(row)

        table = service.GetAiTable()
        self.assertEqual(table, correct_table)
        
    def test_HitAi_EmptyCellHit_CellTypeChangedToMinus(self):
        player_table = PlayTable()
        AI_table = PlayTable()
        service = ServiceGame(player_table,AI_table)
        service.InitializeTable("ui", "white", "AI")
        service.InitializeTable("ui","grey","NAI")
        service.AddAiPlane(3, 0, "ui")
        service.HitAi(7, 7)
        
        correct_table = []
        for i in range(8):
            row = []
            for j in range(8):
                if (i == 1 and j == 1) or ((i == 2 and j == 1) or (i == 2 and j == 3)) or (i == 3 and ( j == 1 or j == 2 or j == 3)) or ((i == 4 and j == 1) or (i == 4 and j == 3)) or (i == 5 and j == 1):
                    cell = ButtonForRepo("1",i,j,"blue","AI")
                elif i == 7 and j == 7:
                    cell = ButtonForRepo("-",i,j,"X","AI")
                elif i == 3 and j == 0:
                    cell = ButtonForRepo("1",i,j,"pink","AI")
                else:
                    cell = ButtonForRepo("0",i,j,"white","AI")
                row.append(cell)
            correct_table.append(row)

        table = service.GetAiTable()
        self.assertEqual(table, correct_table)
    
    def test_HitAi_CockPitHit_AllPlaneChangedToX(self):
        player_table = PlayTable()
        AI_table = PlayTable()
        service = ServiceGame(player_table,AI_table)
        service.InitializeTable("ui", "white", "AI")
        service.InitializeTable("ui","grey","NAI")
        service.AddAiPlane(3, 0, "ui")
        service.HitAi(3, 0)
        
        correct_table = []
        for i in range(8):
            row = []
            for j in range(8):
                if (i == 1 and j == 1) or ((i == 2 and j == 1) or (i == 2 and j == 3)) or (i == 3 and ( j == 1 or j == 2 or j == 3)) or ((i == 4 and j == 1) or (i == 4 and j == 3)) or (i == 5 and j == 1):
                    cell = ButtonForRepo("X",i,j,"X","AI")
                elif i == 3 and j == 0:
                    cell = ButtonForRepo("X",i,j,"X","AI")
                else:
                    cell = ButtonForRepo("0",i,j,"white","AI")
                row.append(cell)
            correct_table.append(row)

        table = service.GetAiTable()
        self.assertEqual(table, correct_table)
    
    def RunAllTests(self):
        self.test_AddAiPlane_ValidInput_PlaneAddedOnTheTable()
        self.test_AddPlayerPlane_ValidInput_PlaneAddedOnTheTable()
        self.test_HitAi_CockPitHit_AllPlaneChangedToX()
        self.test_HitAi_EmptyCellHit_CellTypeChangedToMinus()
        self.test_HitAi_RandomPartOfPlaneHit_CellTypeChangedToX()
        self.test_InitializeTable_ValidInput_TableInitilizedCorectly()
        self.test_Reset_ValidInput_TablesReseted()

