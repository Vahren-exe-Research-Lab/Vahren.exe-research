# PEER_SCRIPT01 RTTI class inventory — ver0.67 Vahren.exe (2026-10-11)

The EXE keeps MSVC RTTI. These are the **original C++ class names** (194 type descriptors; 180 classes have a recoverable vftable).
Source: RTTI Complete Object Locator → TypeDescriptor → ClassHierarchyDescriptor walk over a verified copy (SHA-256 E8DAC301…767187).
`methods` = number of virtual-function slots up to the next locator, so it is an upper bound. Method names follow `Class::vfNN` and also appear in the named decompilation bundle.

| class | vftable | this offset | virtual slots | inheritance (self→base) |
|---|---|---:|---:|---|
| `?$basic_ios@DU?$char_traits@D@std@@@std` | `0x638434` | 0 | 1 | ?$basic_ios@DU?$char_traits@D@std@@@std → ios_base@std → ?$_Iosb@H@std |
| `?$basic_istream@DU?$char_traits@D@std@@@std` | `0x63847c` | 16 | 1 | ?$basic_istream@DU?$char_traits@D@std@@@std → ?$basic_ios@DU?$char_traits@D@std@@@std → ios_base@std → ?$_Iosb@H@std |
| `?$basic_istringstream@DU?$char_traits@D@std@@V?$allocator@D@2@@std` | `0x6384cc` | 88 | 1 | ?$basic_istringstream@DU?$char_traits@D@std@@V?$allocator@D@2@@std → ?$basic_istream@DU?$char_traits@D@std@@@std → ?$basic_ios@DU?$char_traits@D@std@@@std → ios_base@std → ?$_Iosb@H@std |
| `?$basic_ostream@DU?$char_traits@D@std@@@std` | `0x638484` | 8 | 1 | ?$basic_ostream@DU?$char_traits@D@std@@@std → ?$basic_ios@DU?$char_traits@D@std@@@std → ios_base@std → ?$_Iosb@H@std |
| `?$basic_ostringstream@DU?$char_traits@D@std@@V?$allocator@D@2@@std` | `0x6384dc` | 80 | 1 | ?$basic_ostringstream@DU?$char_traits@D@std@@V?$allocator@D@2@@std → ?$basic_ostream@DU?$char_traits@D@std@@@std → ?$basic_ios@DU?$char_traits@D@std@@@std → ios_base@std → ?$_Iosb@H@std |
| `?$basic_streambuf@DU?$char_traits@D@std@@@std` | `0x63843c` | 0 | 15 | ?$basic_streambuf@DU?$char_traits@D@std@@@std |
| `?$basic_stringbuf@DU?$char_traits@D@std@@V?$allocator@D@2@@std` | `0x63848c` | 0 | 15 | ?$basic_stringbuf@DU?$char_traits@D@std@@V?$allocator@D@2@@std → ?$basic_streambuf@DU?$char_traits@D@std@@@std |
| `?$ctype@D@std` | `0x6384ec` | 0 | 9 | ?$ctype@D@std → ctype_base@std → facet@locale@std |
| `A_Chara` | `0x638cbc` | 0 | 21 | A_Chara → Chara → Actionable |
| `Actionable` | `0x637f74` | 0 | 6 | Actionable |
| `AllLifeWnd` | `0x637e64` | 0 | 21 | AllLifeWnd → FrameWnd → FrontView → Actionable → NoDeletedObject |
| `AllLifeWnd` | `0x637ebc` | 40 | 6 | AllLifeWnd → FrameWnd → FrontView → Actionable → NoDeletedObject |
| `ArmyChip@ArmyChipBuilder` | `0x63ae74` | 0 | 21 | ArmyChip@ArmyChipBuilder → Chara → Actionable |
| `ArmyChipBuilder` | `0x63ae54` | 0 | 6 | ArmyChipBuilder → Actionable |
| `AttackRays` | `0x63a7a4` | 0 | 21 | AttackRays → A_Chara → Chara → Actionable |
| `BattleCut` | `0x637f90` | 0 | 3 | BattleCut → FrontView → Actionable → NoDeletedObject |
| `BattleCut` | `0x637fa0` | 40 | 6 | BattleCut → FrontView → Actionable → NoDeletedObject |
| `BattleCut_right` | `0x63a75c` | 0 | 3 | BattleCut_right → BattleCut → FrontView → Actionable → NoDeletedObject |
| `BattleCut_right` | `0x63a76c` | 40 | 6 | BattleCut_right → BattleCut → FrontView → Actionable → NoDeletedObject |
| `BattleMsg` | `0x637f1c` | 0 | 21 | BattleMsg → A_Chara → Chara → Actionable → NoDeletedObject |
| `BattleStatusWnd` | `0x637fbc` | 0 | 21 | BattleStatusWnd → FadeWnd → FrameWnd → FrontView → Actionable → NoDeletedObject |
| `BattleStatusWnd` | `0x638014` | 40 | 6 | BattleStatusWnd → FadeWnd → FrameWnd → FrontView → Actionable → NoDeletedObject |
| `BattleVSync` | `0x63a788` | 0 | 6 | BattleVSync → Actionable → NoDeletedObject |
| `BattleWnd` | `0x638074` | 0 | 21 | BattleWnd → FadeWnd → FrameWnd → FrontView → Actionable → NoDeletedObject |
| `BattleWnd` | `0x6380cc` | 40 | 6 | BattleWnd → FadeWnd → FrameWnd → FrontView → Actionable → NoDeletedObject |
| `Blind` | `0x63afd4` | 0 | 1 | Blind → BlindFilter@GameModel → A_Chara → Chara → Actionable → NoDeletedObject |
| `Blind` | `0x63afdc` | 4 | 21 | Blind → BlindFilter@GameModel → A_Chara → Chara → Actionable → NoDeletedObject |
| `Block` | `0x6392bc` | 0 | 21 | Block → S_Chara → Chara → Actionable → NoDeletedObject |
| `ButtonFlashMark` | `0x638c28` | 0 | 3 | ButtonFlashMark → FrontView → Actionable → NoDeletedObject |
| `ButtonFlashMark` | `0x638c38` | 40 | 6 | ButtonFlashMark → FrontView → Actionable → NoDeletedObject |
| `BuyWnd` | `0x6380ec` | 0 | 21 | BuyWnd → FadeWnd → FrameWnd → FrontView → Actionable → NoDeletedObject |
| `BuyWnd` | `0x638144` | 40 | 6 | BuyWnd → FadeWnd → FrameWnd → FrontView → Actionable → NoDeletedObject |
| `Castler` | `0x63af24` | 0 | 21 | Castler → A_Chara → Chara → Actionable |
| `Chara` | `0x638164` | 0 | 21 | Chara → Actionable |
| `CharaWnd` | `0x6381bc` | 0 | 21 | CharaWnd → FadeWnd → FrameWnd → FrontView → Actionable → NoDeletedObject |
| `CharaWnd` | `0x638214` | 40 | 6 | CharaWnd → FadeWnd → FrameWnd → FrontView → Actionable → NoDeletedObject |
| `ChildOwner` | `0x63a98c` | 0 | 21 | ChildOwner → Chara → Actionable |
| `ChoiceWnd` | `0x638234` | 0 | 22 | ChoiceWnd → FrameWnd → FrontView → Actionable → NoDeletedObject |
| `ChoiceWnd` | `0x638290` | 40 | 6 | ChoiceWnd → FrameWnd → FrontView → Actionable → NoDeletedObject |
| `CircleMark` | `0x63ab74` | 0 | 21 | CircleMark → S_Chara → Chara → Actionable → NoDeletedObject |
| `CircleRays` | `0x63a7fc` | 0 | 21 | CircleRays → A_Chara → Chara → Actionable |
| `CorpsWnd` | `0x6382cc` | 0 | 21 | CorpsWnd → FrameWnd → FrontView → Actionable → NoDeletedObject |
| `CorpsWnd` | `0x638324` | 40 | 6 | CorpsWnd → FrameWnd → FrontView → Actionable → NoDeletedObject |
| `Corpse` | `0x63ac7c` | 0 | 21 | Corpse → Chara → Actionable → NoDeletedObject |
| `Cutin` | `0x638340` | 0 | 3 | Cutin → FrontView → Actionable |
| `Cutin` | `0x638350` | 40 | 6 | Cutin → FrontView → Actionable |
| `CutinBuilder` | `0x63836c` | 0 | 6 | CutinBuilder → Actionable |
| `CutinFantom` | `0x638388` | 0 | 3 | CutinFantom → FrontView → Actionable |
| `CutinFantom` | `0x638398` | 40 | 6 | CutinFantom → FrontView → Actionable |
| `DGoal` | `0x6394c4` | 0 | 21 | DGoal → Block → S_Chara → Chara → Actionable → NoDeletedObject |
| `DItem` | `0x639574` | 0 | 21 | DItem → DGoal → Block → S_Chara → Chara → Actionable → NoDeletedObject |
| `DStart` | `0x63951c` | 0 | 21 | DStart → DGoal → Block → S_Chara → Chara → Actionable → NoDeletedObject |
| `DemoPerson` | `0x638030` | 0 | 8 | DemoPerson → Enemy → Person → Actionable → NoDeletedObject |
| `DemoPerson` | `0x638054` | 144 | 6 | DemoPerson → Enemy → Person → Actionable → NoDeletedObject |
| `DestinationMark` | `0x63ac24` | 0 | 21 | DestinationMark → S_Chara → Chara → Actionable → NoDeletedObject |
| `Detail2Wnd` | `0x6388f4` | 0 | 21 | Detail2Wnd → FadeWnd → FrameWnd → FrontView → Actionable → NoDeletedObject |
| `Detail2Wnd` | `0x63894c` | 40 | 6 | Detail2Wnd → FadeWnd → FrameWnd → FrontView → Actionable → NoDeletedObject |
| `DetailWnd` | `0x63896c` | 0 | 21 | DetailWnd → FadeWnd → FrameWnd → FrontView → Actionable → NoDeletedObject |
| `DetailWnd` | `0x6389c4` | 40 | 6 | DetailWnd → FadeWnd → FrameWnd → FrontView → Actionable → NoDeletedObject |
| `DialogWnd` | `0x6389fc` | 0 | 21 | DialogWnd → FrameWnd → FrontView → Actionable → NoDeletedObject |
| `DialogWnd` | `0x638a54` | 40 | 6 | DialogWnd → FrameWnd → FrontView → Actionable → NoDeletedObject |
| `DiploWnd` | `0x638a74` | 0 | 21 | DiploWnd → FadeWnd → FrameWnd → FrontView → Actionable → NoDeletedObject |
| `DiploWnd` | `0x638acc` | 40 | 6 | DiploWnd → FadeWnd → FrameWnd → FrontView → Actionable → NoDeletedObject |
| `Discus` | `0x63a37c` | 0 | 21 | Discus → A_Chara → Chara → Actionable → NoDeletedObject |
| `Dot` | `0x639a4c` | 0 | 22 | Dot → S_Chara → Chara → Actionable → NoDeletedObject |
| `DragChara` | `0x639b48` | 0 | 3 | DragChara → FrontView |
| `DungeonSheetSkin` | `0x63a43c` | 0 | 3 | DungeonSheetSkin → FrontView |
| `DungeonWnd` | `0x638aec` | 0 | 21 | DungeonWnd → FadeWnd → FrameWnd → FrontView → Actionable → NoDeletedObject |
| `DungeonWnd` | `0x638b44` | 40 | 6 | DungeonWnd → FadeWnd → FrameWnd → FrontView → Actionable → NoDeletedObject |
| `Enemy` | `0x638b60` | 0 | 8 | Enemy → Person → Actionable → NoDeletedObject |
| `Enemy` | `0x638b84` | 144 | 6 | Enemy → Person → Actionable → NoDeletedObject |
| `ExpresBin` | `0x639650` | 0 | 3 | ExpresBin → ExpresElement |
| `ExpresFunc` | `0x639640` | 0 | 3 | ExpresFunc → ExpresElement |
| `ExpresNum` | `0x638de0` | 0 | 3 | ExpresNum → ExpresElement |
| `ExpresString` | `0x638538` | 0 | 3 | ExpresString → ExpresElement |
| `FadeInSheet` | `0x638d84` | 0 | 7 | FadeInSheet → FadeSheet → Sheet → Actionable |
| `FadeMessageSheet` | `0x638dc0` | 0 | 7 | FadeMessageSheet → MessageSheet → Sheet → Actionable |
| `FadeOutSheet` | `0x6388d4` | 0 | 7 | FadeOutSheet → FadeSheet → Sheet → Actionable |
| `FadeSheet` | `0x63a49c` | 0 | 7 | FadeSheet → Sheet → Actionable |
| `FadeSheetSkin` | `0x63a42c` | 0 | 3 | FadeSheetSkin → FrontView |
| `FieldData` | `0x638c54` | 0 | 21 | FieldData → S_Chara → Chara → Actionable |
| `FlashObj` | `0x6393c4` | 0 | 21 | FlashObj → F_Chara → Chara → Actionable |
| `FlyText` | `0x639314` | 0 | 21 | FlyText → F_Chara → Chara → Actionable |
| `FormationFlash` | `0x63a3d4` | 0 | 21 | FormationFlash → A_Chara → Chara → Actionable |
| `FrameWnd` | `0x638bb4` | 0 | 21 | FrameWnd → FrontView → Actionable → NoDeletedObject |
| `FrameWnd` | `0x638c0c` | 40 | 6 | FrameWnd → FrontView → Actionable → NoDeletedObject |
| `FrontView` | `0x638cac` | 0 | 3 | FrontView |
| `FrontViewAttach` | `0x638da4` | 0 | 6 | FrontViewAttach → Actionable |
| `GameCtrl` | `0x638d34` | 0 | 6 | GameCtrl → Actionable → NoDeletedObject |
| `GameEvent` | `0x63a6d0` | 0 | 6 | GameEvent → Actionable → NoDeletedObject |
| `GameException` | `0x638ba4` | 0 | 2 | GameException → exception@std |
| `GameManager` | `0x638df0` | 0 | 10 | GameManager → GameMngBase |
| `GameMngBase` | `0x638e1c` | 0 | 10 | GameMngBase |
| `GameModel` | `0x638e48` | 0 | 3 | GameModel |
| `GameMouse` | `0x638e58` | 0 | 3 | GameMouse |
| `GameTask` | `0x638e68` | 0 | 1 | GameTask |
| `GameView` | `0x638e70` | 0 | 1 | GameView |
| `GameWindow` | `0x638e78` | 0 | 1 | GameWindow |
| `GroupWnd` | `0x638e84` | 0 | 21 | GroupWnd → FrameWnd → FrontView → Actionable → NoDeletedObject |
| `GroupWnd` | `0x638edc` | 40 | 6 | GroupWnd → FrameWnd → FrontView → Actionable → NoDeletedObject |
| `Heal` | `0x63a604` | 0 | 21 | Heal → F_Chara → Chara → Actionable → Damager |
| `HelpWnd` | `0x638efc` | 0 | 21 | HelpWnd → FrameWnd → FrontView → Actionable → NoDeletedObject |
| `HelpWnd` | `0x638f54` | 40 | 6 | HelpWnd → FrameWnd → FrontView → Actionable → NoDeletedObject |
| `HeroFlagObj` | `0x63aecc` | 0 | 21 | HeroFlagObj → Chara → Actionable → NoDeletedObject |
| `HeroMemberWnd` | `0x638f74` | 0 | 21 | HeroMemberWnd → FadeWnd → FrameWnd → FrontView → Actionable → NoDeletedObject |
| `HeroMemberWnd` | `0x638fcc` | 40 | 6 | HeroMemberWnd → FadeWnd → FrameWnd → FrontView → Actionable → NoDeletedObject |
| `HeroMenuWnd` | `0x638fec` | 0 | 21 | HeroMenuWnd → FadeWnd → FrameWnd → FrontView → Actionable → NoDeletedObject |
| `HeroMenuWnd` | `0x639044` | 40 | 6 | HeroMenuWnd → FadeWnd → FrameWnd → FrontView → Actionable → NoDeletedObject |
| `LifeBar` | `0x63abcc` | 0 | 21 | LifeBar → S_Chara → Chara → Actionable → NoDeletedObject |
| `LoadException` | `0x63852c` | 0 | 2 | LoadException → exception@std |
| `LoadWnd` | `0x639064` | 0 | 21 | LoadWnd → FadeWnd → FrameWnd → FrontView → Actionable → NoDeletedObject |
| `LoadWnd` | `0x6390bc` | 40 | 6 | LoadWnd → FadeWnd → FrameWnd → FrontView → Actionable → NoDeletedObject |
| `MenuText` | `0x63a704` | 0 | 21 | MenuText → A_Chara → Chara → Actionable → NoDeletedObject |
| `MenuWnd` | `0x6390dc` | 0 | 21 | MenuWnd → FadeWnd → FrameWnd → FrontView → Actionable → NoDeletedObject |
| `MenuWnd` | `0x639134` | 40 | 6 | MenuWnd → FadeWnd → FrameWnd → FrontView → Actionable → NoDeletedObject |
| `MercenaryWnd` | `0x639154` | 0 | 21 | MercenaryWnd → FadeWnd → FrameWnd → FrontView → Actionable → NoDeletedObject |
| `MercenaryWnd` | `0x6391ac` | 40 | 6 | MercenaryWnd → FadeWnd → FrameWnd → FrontView → Actionable → NoDeletedObject |
| `MessageSheet` | `0x63a47c` | 0 | 7 | MessageSheet → Sheet → Actionable |
| `MessageSheetSkin` | `0x63a44c` | 0 | 3 | MessageSheetSkin → FrontView |
| `MessageWnd` | `0x6391cc` | 0 | 21 | MessageWnd → FadeWnd → FrameWnd → FrontView → Actionable → NoDeletedObject → MsgMark |
| `MessageWnd` | `0x639224` | 40 | 6 | MessageWnd → FadeWnd → FrameWnd → FrontView → Actionable → NoDeletedObject → MsgMark |
| `MiniMapWnd` | `0x639244` | 0 | 21 | MiniMapWnd → FrameWnd → FrontView → Actionable → NoDeletedObject |
| `MiniMapWnd` | `0x63929c` | 40 | 6 | MiniMapWnd → FrameWnd → FrontView → Actionable → NoDeletedObject |
| `Missile` | `0x63a544` | 0 | 23 | Missile → F_Chara → Chara → Actionable → Damager |
| `Mosaic` | `0x63af7c` | 0 | 21 | Mosaic → A_Chara → Chara → Actionable → NoDeletedObject |
| `MsgNextMark` | `0x639b58` | 0 | 3 | MsgNextMark → FrontView |
| `NameLabelWnd` | `0x63941c` | 0 | 21 | NameLabelWnd → FadeWnd → FrameWnd → FrontView → Actionable → NoDeletedObject → MsgMark |
| `NameLabelWnd` | `0x639474` | 40 | 6 | NameLabelWnd → FadeWnd → FrameWnd → FrontView → Actionable → NoDeletedObject → MsgMark |
| `NewGameModel` | `0x639490` | 0 | 3 | NewGameModel → GameModel |
| `NewGameMouse` | `0x6394a0` | 0 | 3 | NewGameMouse → GameMouse |
| `NewGameStage` | `0x63a6ec` | 0 | 4 | NewGameStage → GameStage |
| `NumberText` | `0x63936c` | 0 | 21 | NumberText → F_Chara → Chara → Actionable |
| `OggDecoder` | `0x6395cc` | 0 | 5 | OggDecoder → PCMDecoder |
| `PCMDecoder` | `0x6395e4` | 0 | 5 | PCMDecoder |
| `ParseException` | `0x639634` | 0 | 2 | ParseException → exception@std |
| `PathArrow` | `0x63a2f8` | 0 | 3 | PathArrow → FrontView |
| `PauseWnd` | `0x63966c` | 0 | 21 | PauseWnd → FrameWnd → FrontView → Actionable → NoDeletedObject |
| `PauseWnd` | `0x6396c4` | 40 | 6 | PauseWnd → FrameWnd → FrontView → Actionable → NoDeletedObject |
| `Person` | `0x6396e0` | 0 | 8 | Person |
| `PersonSelectWnd` | `0x639944` | 0 | 21 | PersonSelectWnd → FadeWnd → FrameWnd → FrontView → Actionable → NoDeletedObject |
| `PersonSelectWnd` | `0x63999c` | 40 | 6 | PersonSelectWnd → FadeWnd → FrameWnd → FrontView → Actionable → NoDeletedObject |
| `PersonsInfoWnd` | `0x6398cc` | 0 | 21 | PersonsInfoWnd → FadeWnd → FrameWnd → FrontView → Actionable → NoDeletedObject |
| `PersonsInfoWnd` | `0x639924` | 40 | 6 | PersonsInfoWnd → FadeWnd → FrameWnd → FrontView → Actionable → NoDeletedObject |
| `PictureWnd` | `0x6399bc` | 0 | 21 | PictureWnd → FadeWnd → FrameWnd → FrontView → Actionable → NoDeletedObject → MsgMark |
| `PictureWnd` | `0x639a14` | 40 | 6 | PictureWnd → FadeWnd → FrameWnd → FrontView → Actionable → NoDeletedObject → MsgMark |
| `Player` | `0x639b08` | 0 | 8 | Player → Enemy → Person → Actionable → NoDeletedObject |
| `Player` | `0x639b2c` | 144 | 6 | Player → Enemy → Person → Actionable → NoDeletedObject |
| `PoliWnd` | `0x63a274` | 0 | 21 | PoliWnd → FadeWnd → FrameWnd → FrontView → Actionable → NoDeletedObject |
| `PoliWnd` | `0x63a2cc` | 40 | 6 | PoliWnd → FadeWnd → FrameWnd → FrontView → Actionable → NoDeletedObject |
| `PoliticsWnd` | `0x63a1fc` | 0 | 21 | PoliticsWnd → FadeWnd → FrameWnd → FrontView → Actionable → NoDeletedObject |
| `PoliticsWnd` | `0x63a254` | 40 | 6 | PoliticsWnd → FadeWnd → FrameWnd → FrontView → Actionable → NoDeletedObject |
| `PowerSelectWnd` | `0x63a184` | 0 | 21 | PowerSelectWnd → FadeWnd → FrameWnd → FrontView → Actionable → NoDeletedObject |
| `PowerSelectWnd` | `0x63a1dc` | 40 | 6 | PowerSelectWnd → FadeWnd → FrameWnd → FrontView → Actionable → NoDeletedObject |
| `PowersInfoWnd` | `0x639dc4` | 0 | 21 | PowersInfoWnd → FadeWnd → FrameWnd → FrontView → Actionable → NoDeletedObject |
| `PowersInfoWnd` | `0x639e1c` | 40 | 6 | PowersInfoWnd → FadeWnd → FrameWnd → FrontView → Actionable → NoDeletedObject |
| `RetreatVoice` | `0x63ab1c` | 0 | 21 | RetreatVoice → Chara → Actionable → NoDeletedObject |
| `RushMissile` | `0x63a6b4` | 0 | 6 | RushMissile → Actionable → NoDeletedObject |
| `SaveWnd` | `0x639d4c` | 0 | 21 | SaveWnd → FadeWnd → FrameWnd → FrontView → Actionable → NoDeletedObject |
| `SaveWnd` | `0x639da4` | 40 | 6 | SaveWnd → FadeWnd → FrameWnd → FrontView → Actionable → NoDeletedObject |
| `ScenarioSelectWnd` | `0x63a01c` | 0 | 21 | ScenarioSelectWnd → FadeWnd → FrameWnd → FrontView → Actionable → NoDeletedObject |
| `ScenarioSelectWnd` | `0x63a074` | 40 | 6 | ScenarioSelectWnd → FadeWnd → FrameWnd → FrontView → Actionable → NoDeletedObject |
| `ScenarioText2Wnd` | `0x63a10c` | 0 | 21 | ScenarioText2Wnd → ScenarioTextWnd → FadeWnd → FrameWnd → FrontView → Actionable → NoDeletedObject |
| `ScenarioText2Wnd` | `0x63a164` | 40 | 6 | ScenarioText2Wnd → ScenarioTextWnd → FadeWnd → FrameWnd → FrontView → Actionable → NoDeletedObject |
| `ScenarioTextWnd` | `0x63a094` | 0 | 21 | ScenarioTextWnd → FadeWnd → FrameWnd → FrontView → Actionable → NoDeletedObject |
| `ScenarioTextWnd` | `0x63a0ec` | 40 | 6 | ScenarioTextWnd → FadeWnd → FrameWnd → FrontView → Actionable → NoDeletedObject |
| `ScriptBattle` | `0x63862c` | 0 | 1 | ScriptBattle → ScriptElement |
| `ScriptBlock` | `0x638d24` | 0 | 1 | ScriptBlock → ScriptElement |
| `ScriptData` | `0x638d1c` | 0 | 1 | ScriptData → ScriptElement |
| `ScriptFunc` | `0x638634` | 0 | 1 | ScriptFunc → ScriptElement |
| `ScriptIF` | `0x63962c` | 0 | 1 | ScriptIF → ScriptElement |
| `ScriptSet` | `0x638d2c` | 0 | 1 | ScriptSet → ScriptElement |
| `ScriptWhile` | `0x639660` | 0 | 1 | ScriptWhile → ScriptElement |
| `ScrollDot` | `0x639aac` | 0 | 22 | ScrollDot → Dot → S_Chara → Chara → Actionable → NoDeletedObject |
| `SelectedRect` | `0x63a2e8` | 0 | 3 | SelectedRect → FrontView |
| `Sheet` | `0x63a45c` | 0 | 7 | Sheet → Actionable |
| `ShotTargetFlag` | `0x63a30c` | 0 | 21 | ShotTargetFlag → A_Chara → Chara → Actionable → NoDeletedObject |
| `SickFlash` | `0x63aac4` | 0 | 21 | SickFlash → Chara → Actionable → NoDeletedObject |
| `SimpleMissile` | `0x63a5a4` | 0 | 23 | SimpleMissile → Missile → F_Chara → Chara → Actionable → Damager |
| `SimpleStaticUnit` | `0x63a8e4` | 0 | 33 | SimpleStaticUnit → StaticUnit → Unit → ChildOwner → Chara → Actionable → Damager → NoDeletedObject |
| `SimpleUnit` | `0x63a4bc` | 0 | 33 | SimpleUnit → Unit → ChildOwner → Chara → Actionable → Damager → NoDeletedObject |
| `Spot` | `0x6385bc` | 0 | 27 | Spot → SpotElm → S_Chara → Chara → Actionable → NoDeletedObject |
| `SpotBloom` | `0x63879c` | 0 | 21 | SpotBloom → A_Chara → Chara → Actionable → NoDeletedObject |
| `SpotElm` | `0x63854c` | 0 | 27 | SpotElm → S_Chara → Chara → Actionable |
| `SpotEscapePath` | `0x638864` | 0 | 27 | SpotEscapePath → SpotPath → SpotElm → S_Chara → Chara → Actionable → NoDeletedObject |
| `SpotFire` | `0x638744` | 0 | 21 | SpotFire → Chara → Actionable → NoDeletedObject |
| `SpotFlag` | `0x638694` | 0 | 21 | SpotFlag → A_Chara → Chara → Actionable → NoDeletedObject |
| `SpotLabel` | `0x63863c` | 0 | 21 | SpotLabel → A_Chara → Chara → Actionable → NoDeletedObject |
| `SpotMark` | `0x6386ec` | 0 | 21 | SpotMark → A_Chara → Chara → Actionable → NoDeletedObject |
| `SpotPath` | `0x6387f4` | 0 | 27 | SpotPath → SpotElm → S_Chara → Chara → Actionable → NoDeletedObject |
| `StaticUnit` | `0x63a85c` | 0 | 33 | StaticUnit → Unit → ChildOwner → Chara → Actionable → Damager → NoDeletedObject |
| `StatusWnd` | `0x639c5c` | 0 | 21 | StatusWnd → FadeWnd → FrameWnd → FrontView → Actionable → NoDeletedObject |
| `StatusWnd` | `0x639cb4` | 40 | 6 | StatusWnd → FadeWnd → FrameWnd → FrontView → Actionable → NoDeletedObject |
| `SummonFlash` | `0x63a65c` | 0 | 21 | SummonFlash → F_Chara → Chara → Actionable |
| `TempStatusWnd` | `0x639cd4` | 0 | 21 | TempStatusWnd → StatusWnd → FadeWnd → FrameWnd → FrontView → Actionable → NoDeletedObject |
| `TempStatusWnd` | `0x639d2c` | 40 | 6 | TempStatusWnd → StatusWnd → FadeWnd → FrameWnd → FrontView → Actionable → NoDeletedObject |
| `TimeWnd` | `0x639fa4` | 0 | 21 | TimeWnd → FrameWnd → FrontView → Actionable → NoDeletedObject |
| `TimeWnd` | `0x639ffc` | 40 | 6 | TimeWnd → FrameWnd → FrontView → Actionable → NoDeletedObject |
| `ToolWnd` | `0x639b6c` | 0 | 21 | ToolWnd → FadeWnd → FrameWnd → FrontView → Actionable → NoDeletedObject |
| `ToolWnd` | `0x639bc4` | 40 | 6 | ToolWnd → FadeWnd → FrameWnd → FrontView → Actionable → NoDeletedObject |
| `Troop` | `0x639a30` | 0 | 6 | Troop → Actionable → NoDeletedObject |
| `Troop2Wnd` | `0x639f2c` | 0 | 21 | Troop2Wnd → TroopWnd → FrameWnd → FrontView → Actionable → NoDeletedObject |
| `Troop2Wnd` | `0x639f84` | 40 | 6 | Troop2Wnd → TroopWnd → FrameWnd → FrontView → Actionable → NoDeletedObject |
| `TroopWnd` | `0x639eb4` | 0 | 21 | TroopWnd → FrameWnd → FrontView → Actionable → NoDeletedObject |
| `TroopWnd` | `0x639f0c` | 40 | 6 | TroopWnd → FrameWnd → FrontView → Actionable → NoDeletedObject |
| `TurnWnd` | `0x639e3c` | 0 | 21 | TurnWnd → FrameWnd → FrontView → Actionable → NoDeletedObject |
| `TurnWnd` | `0x639e94` | 40 | 6 | TurnWnd → FrameWnd → FrontView → Actionable → NoDeletedObject |
| `Unit` | `0x63a9e4` | 0 | 33 | Unit → ChildOwner → Chara → Actionable → Damager → NoDeletedObject |
| `UnitFlash` | `0x63aa6c` | 0 | 21 | UnitFlash → Chara → Actionable → NoDeletedObject |
| `ViewEdge` | `0x638d14` | 0 | 1 | ViewEdge |
| `WarWnd` | `0x639be4` | 0 | 21 | WarWnd → FadeWnd → FrameWnd → FrontView → Actionable → NoDeletedObject |
| `WarWnd` | `0x639c3c` | 40 | 6 | WarWnd → FadeWnd → FrameWnd → FrontView → Actionable → NoDeletedObject |
| `Weapon` | `0x63acd4` | 0 | 21 | Weapon → S_Chara → Chara → Actionable → NoDeletedObject |
| `_Generic_error_category@std` | `0x609824` | 0 | 6 | _Generic_error_category@std → error_category@std |
| `_Iostream_error_category@std` | `0x609858` | 0 | 6 | _Iostream_error_category@std → error_category@std |
| `_Locimp@locale@std` | `0x6098c8` | 0 | 1 | _Locimp@locale@std → facet@locale@std |
| `_System_error_category@std` | `0x60987c` | 0 | 6 | _System_error_category@std → _Generic_error_category@std → error_category@std |
| `__non_rtti_object@std` | `0x60990c` | 0 | 2 | __non_rtti_object@std → bad_typeid@std → exception@std |
| `bad_alloc@std` | `0x609840` | 0 | 2 | bad_alloc@std → exception@std |
| `bad_cast@std` | `0x6098f4` | 0 | 2 | bad_cast@std → exception@std |
| `bad_exception@std` | `0x609b00` | 0 | 2 | bad_exception@std → exception@std |
| `bad_typeid@std` | `0x609900` | 0 | 2 | bad_typeid@std → exception@std |
| `error_category@std` | `0x609800` | 0 | 6 | error_category@std |
| `exception@std` | `0x6098d4` | 0 | 2 | exception@std |
| `facet@locale@std` | `0x6098bc` | 0 | 1 | facet@locale@std |
| `failure@ios_base@std` | `0x638520` | 0 | 2 | failure@ios_base@std → system_error@std → runtime_error@std → exception@std |
| `ios_base@std` | `0x63842c` | 0 | 1 | ios_base@std → ?$_Iosb@H@std |
| `length_error@std` | `0x6097dc` | 0 | 2 | length_error@std → logic_error@std → exception@std |
| `logic_error@std` | `0x6097d0` | 0 | 2 | logic_error@std → exception@std |
| `out_of_range@std` | `0x6097e8` | 0 | 2 | out_of_range@std → logic_error@std → exception@std |
| `runtime_error@std` | `0x6097f4` | 0 | 2 | runtime_error@std → exception@std |
| `system_error@std` | `0x638514` | 0 | 2 | system_error@std → runtime_error@std → exception@std |
| `type_info` | `0x609918` | 0 | 1 | type_info |

vftable rows: 232

## Key classes for the reimplementation
- Script AST: `ScriptElement` ← `ScriptFunc` / `ScriptIF` / `ScriptWhile` / `ScriptBlock` / `ScriptBattle` / `ScriptSet` / `ScriptData`
- Expressions: `ExpresElement` ← `ExpresNum` / `ExpresString` / `ExpresBin` / `ExpresFunc` (vf00=evalInt, vf01=evalString, vf02=isString)
- Flow-control exceptions: `BreakError`, `ContinueError`, `ParseException`, `LoadException`, `GameException`
- Game objects: `Unit`, `SimpleUnit`, `StaticUnit`, `Troop`, `Spot`, `Person`, `Player`, `Enemy`, `Chara` family, `Missile`, `Weapon`, `Damager`, `Heal`
- Engine/UI: `GameModel`, `NewGameModel`, `GameManager`, `GameStage`, `GameView`, plus about 60 `*Wnd` window classes and the `*Sheet` scene-effect classes (`FadeOutSheet` etc.)
- Audio: `OggDecoder`, `PCMDecoder`