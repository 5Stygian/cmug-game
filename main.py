from cmu_graphics import *
app.title = "cmug game"

from typing import Dict

class Menu(Rect):
    MENUS   = []
    BUTTONS = []
    TITLES  = []
    
    def __init__(self, *args, parent = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.parent = parent
        if self.parent:
            if type(self.parent) != Menu:
                raise TypeError(f"parent must be of type Menu, not {self.parent.__class__.__name__}")
            else:
                self.centerX = (parent.centerX - self.width/2) + self.centerX
                self.top = parent.top + self.centerY
        
        self.buttons = []
        self.buttonsData = []
        
        self.titles = []
        self.titlesData = []
        
        self.data = {
            "Class": f"{self.__class__.__name__}",
            "Parent": f"{self.parent}",
            "Dimensions": {
                "TopLeft": (self.left, self.top),
                "TopRight": (self.right, self.top),
                "BottomLeft": (self.left, self.bottom),
                "BottomRight": (self.right, self.bottom),
                "Width": self.width,
                "Height": self.height,
            },
            "BackgroundFill": f"{self.fill}",
            "BorderFill": self.border,
            "BorderWidth": self.borderWidth,
            "Opacity": self.opacity,
            "IsVisible": self.visible,
            "Buttons": self.buttonsData,
            "Titles": self.titlesData
        }
        
        Menu.MENUS.append(self.data)
    
    def addEventListener(self, x, y):
        for button in self.buttons:
            if button.contains(x, y) and button.onclick is not None:
                button.onclick()
                break
    
    class Button(Rect):
        def __init__(self, parent, *args, 
                     textValue: str = "", textFill = rgb(0,0,0), textSize: int|float=12.0, textFont: str = "arial", textOpacity: int|float = 100,
                     textIsBold: bool = False, textIsItalic: bool = False, textIsVisible: bool = True,
                     onclick = None, debug: bool = False, **kwargs):
            super().__init__(*args, **kwargs)
            self.parent  = parent
            self.onclick = onclick
            if callable(self.onclick) == False and self.onclick is not None:
                raise TypeError(f"onclick should be a function, not {self.onclick.__class__.__name__}")
            
            self.centerX = (self.parent.centerX - self.width/2) + self.centerX
            self.centerY = self.parent.top + self.centerY
            
            self.textValue = textValue
            self.textFill  = textFill
            self.textSize  = textSize
            self.textFont  = textFont
            self.textIsBold = textIsBold
            self.textIsItalic = textIsItalic
            self.textOpacity = textOpacity
            self.textIsVisible = textIsVisible
            self.text = Label(
                self.textValue,
                self.centerX, self.centerY,
                fill=self.textFill,
                size=self.textSize,
                font=self.textFont,
                bold=self.textIsBold,
                italic=self.textIsItalic,
                opacity=self.textOpacity,
                visible=self.textIsVisible
            )
            
            self.data = {
                "Class": f"{self.__class__.__name__}",
                "Parent": f"{self.parent}",
                "Onclick": f"{self.onclick}",
                "BoundingBox": {
                    "Dimensions": {
                        "TopLeft": (self.left, self.top),
                        "TopRight": (self.right, self.top),
                        "BottomLeft": (self.left, self.bottom),
                        "BottomRight": (self.right, self.bottom),
                        "Width": self.width,
                        "Height": self.height
                    },
                    "BackgroundFill": f"{self.fill}",
                    "BorderFill": self.border,
                    "BorderWidth": self.borderWidth,
                    "Opacity": self.opacity,
                    "IsVisible": self.visible
                },
                "Text": {
                    "Position": (self.text.centerX, self.text.centerY),
                    "Color": f"{self.text.fill}",
                    "Font": self.text.font,
                    "Size": self.text.size,
                    "IsBold": self.text.bold,
                    "IsItalic": self.text.italic,
                    "Opacity": self.text.opacity,
                    "IsVisible": self.text.visible
                }
            }
            
            self.parent.buttons.append(self)
            self.parent.buttonsData.append(self.data)
            Menu.BUTTONS.append(self.data)
            
        def addEventListener(self, x, y) -> None:
            if self.contains(x, y):
                self.onclick()
    
    class Title(Label):
        def __init__(self, parent, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.parent = parent
            
            self.centerX = parent.centerX + self.centerX
            self.top = parent.top + self.centerY
            
            self.data = {
                "Class": f"{self.__class__.__name__}",
                "Parent": f"{self.parent}",
                "Dimensions": {
                    "TopLeft": (self.left, self.top),
                    "TopRight": (self.right, self.top),
                    "BottomLeft": (self.left, self.bottom),
                    "BottomRight": (self.right, self.bottom),
                    "Width": self.width,
                    "Height": self.height,
                },
                "Position": (self.centerX, self.centerY),
                "Value": self.value,
                "Color": f"{self.fill}",
                "Font": self.font,
                "Size": self.size,
                "IsBold": self.bold,
                "IsItalic": self.italic,
                "Opacity": self.opacity,
                "IsVisible": self.visible
            }
            
            self.parent.titles.append(self)
            self.parent.titlesData.append(self.data)
            Menu.TITLES.append(self.data)

class TitledMenu(Menu):
    def __init__(self, titleValue, titleXAlign, titleYAlign, *args, titleSize=15, bold=True, parent=None, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.titleValue = titleValue
        self.titleXAlign = titleXAlign
        self.titleYAlign = titleYAlign
        self.titleSize = titleSize
        self.bold = bold
        self.title = Menu.Title(
            self,
            self.titleValue,
            self.titleXAlign, self.titleYAlign,
            size=self.titleSize,
            bold=self.bold
        )
        self.title.left = self.left + 6
        
        self.dividerLine = Line(
            self.left, self.title.bottom+7,
            self.right, self.title.bottom+7
        )

class VerticalTitle(Menu.Title):
    def __init__(self, *args, spacing=0, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.spacing = self.size + spacing
        
        self.__valueList = list(self.value)
        self.chars = Group()
        
        for _ in range(len(self.__valueList)):
            self.chars.add(
                Menu.Title(
                    self.parent,
                    self.__valueList[_],
                    0, self.centerY+self.spacing*_,
                    fill=self.fill,
                    size=self.size,
                    font=self.font,
                    bold=self.bold,
                    italic=self.italic,
                    opacity=self.opacity,
                    visible=self.visible
                )   
            )
        
        self.chars.centerX = self.centerX
        
        self.visible = False
        
        self.chars.boundingbox = 10
        
        self.data = {
            "Class": f"{self.__class__.__name__}",
            "Parent": f"{self.parent}",
            "Position": (self.chars.centerX, self.chars.centerY),
            "Value": self.value,
            "Color": f"{self.fill}",
            "Font": self.font,
            "Size": self.size,
            "IsBold": self.bold,
            "IsItalic": self.italic,
            "Opacity": self.opacity,
            "IsVisible": self.visible
        }
    
    def getData(self) -> Dict:
        return self.data

#*********************#

Number = int|float

# UI
## Functions
def nav_SwitchToCombatScreen() -> None:
    CombatScreen.visible = True

## Topbar
menu_Topbar = Menu(
    0, 0,
    400, 40,
    fill=app.background
)
menu_Topbar.borderBottom = Line(
    menu_Topbar.left, menu_Topbar.bottom,
    menu_Topbar.right, menu_Topbar.bottom,
    fill=rgb(60,60,60),
    lineWidth=3
)

nav_CombatScreen = Menu.Button(
    menu_Topbar,
    -155, 0,
    90, menu_Topbar.height,
    onclick=nav_SwitchToCombatScreen,
    fill=app.background,
    border=menu_Topbar.borderBottom.fill,
    borderWidth=3,
    textValue="Combat",
    textSize=15,
    textIsBold=True
)

Topbar = Group(
    menu_Topbar, menu_Topbar.borderBottom, 
    nav_CombatScreen, nav_CombatScreen.text
)

# Game Areas
## Combat Screen
menu_CombatScreen = Menu(
    menu_Topbar.borderBottom.x1, menu_Topbar.borderBottom.y1,
    menu_Topbar.borderBottom.x2, app.height-menu_Topbar.height,
    fill=None
)

CombatScreen = Group( menu_CombatScreen )

# Event Listeners
def onMousePress(x: Number, y: Number):
    menu_Topbar.addEventListener(x, y)

cmu_graphics.run() # type: ignore
