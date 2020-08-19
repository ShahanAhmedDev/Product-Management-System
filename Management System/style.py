def searchBoxStyle():
    return """
    QGroupBox{
    background-color:#9bc9ff;
    font:12pt Times Bold;
    color:White;
    border:2px solid gray;
    border-radius: 10px;
    }
    """
def listBoxStyle():
    return """
    QGroupBox{
    background-color:#fcc234;
    font:12pt Arial Bold;
    color:White;
    border:2px solid gray;
    border-radius: 10px;
    }
    """

def searchButtonStyle():
    return """ 
    QPushButton{
    background-color: #fcc324;
    border-style:outset;
    border-width: 1px;
    border-radius: 6px;
    border-color:beige;
    font:12px;
    padding:4px;
    min-width:6em;
    }
    
    """

def listButtonStyle():
    return """
    QPushButton{
    background-color: #9bc9ff;
    border-style:outset;
    border-width: 1px;
    border-radius: 6px;
    border-color:beige;
    font:12px;
    padding:4px;
    min-width:6em;
    }
    """

def productBottomFrame():
    return """
        QFrame{
    font:12pt Times Bold;
    background-color: #fcc324;
    
    }
    """
def productTopFrame():
    return """
    QFrame{
    font:15pt Times Bold;
    background-color:White;
    }
    """

def memberTopFrame():
    return """
        QFrame{
        font:15pt Times Bold;
        background-color:White;
        }
        """

def memberBottomFrame():
    return """
            QFrame{
        font:12pt Times Bold;
        background-color: #fcc324;

        }
        """

def sellProductTopFrame():
    return """
            QFrame{
            font:15pt Times Bold;
            background-color:White;
            }
            """
def sellProductBottomFrame():
    return """
                QFrame{
            font:12pt Times Bold;
            background-color: #fcc324;

            }
            """
def confirmProductTopFrame():
    return """
               QFrame{
               font:15pt Times Bold;
               background-color:White;
               }
               """
def confirmProductBottomFrame():
    return """
                QFrame{
            font:12pt Times Bold;
            background-color: #fcc324;

            }
            """
