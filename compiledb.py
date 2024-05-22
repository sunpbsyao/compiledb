import wx
import ui
import keil
import iar

class CompileDB(ui.UiFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.proj_file = ""

    def __set_proj_file(self, file: str):
        self.proj_file = file
        self.m_project_text.Clear()
        self.m_project_text.AppendText(self.proj_file)

    def m_convert_btnOnButtonClick( self, event ):
        if self.m_projtype_radiobox.GetStringSelection() == "Keil":
            keil.Keil(self.m_project_text.GetLineText(0)).parse()
        elif self.m_projtype_radiobox.GetStringSelection() == "IAR":
            iar.Iar(self.m_project_text.GetLineText(0)).parse()
        wx.MessageBox("转换完成!!!", "提示")
        self.__set_proj_file("")
        
        
    def m_openfile_btnOnButtonClick( self, event ):
        file_dialog = wx.FileDialog(None, "选择工程文件", wildcard="Keil工程文件 (*.uvprojx)|*.uvprojx|IAR工程文件 (*.ewp)|*.ewp|(Makefile;makefile)|Makefile;makefile")
        if file_dialog.ShowModal() == wx.ID_CANCEL:
            return
        self.__set_proj_file(file_dialog.GetPath())

if __name__ == "__main__":
    app = wx.App()
    CompileDB(None).Show()
    app.MainLoop()