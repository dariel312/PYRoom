using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;

namespace PyRoom.WPF
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        public MainWindow()
        {
            InitializeComponent();
        }



        public void MyMessage_KeyDown(object sender, EventArgs e)
        {

            //if (e.Key == Key.Return)
            //    self.submit_message(self.ui.myMessage.Text)
        }

        public void SideBar_ToggleClick(object sender, EventArgs e)
        {
            //         if (self.sidebar.Visibility == Visibility.Collapsed):
            //self.sidebar.Visibility = Visibility.Visible
            // 		else:
            //self.sidebar.Visibility = Visibility.Collapsed

        }
        public void Send_Click(object sender, EventArgs e)
        {


            //self.submit_message(self.ui.myMessage.Text)
        }
        public void Menu_Click(object sender, EventArgs e)
        {

            // sender.ContextMenu.IsOpen = True
        }
        public void Minimize_Click(object sender, EventArgs e)
        {

            //   self.WindowState = WindowState.Minimized
        }
        public void Maximize_Click(object sender, EventArgs e)
        {
            //         if self.WindowState == WindowState.Normal:
            //self.WindowState = WindowState.Maximized
            // 		else:
            //self.WindowState = WindowState.Normal
        }
        public void Exit_Click(object sender, EventArgs e)
        {

            // self.close()
        }
        public void Rectangle_MouseDown(object sender, EventArgs e)
        {
            //         if (e.ChangedButton == MouseButton.Left):
            //if (self.WindowState == WindowState.Maximized):
            //	self.WindowState = WindowState.Normal
            //             self.DragMove()
        }

        public void Menu_Connect_Click(object sender, EventArgs e)
        {
            //      prompt = ConnectPrompt()

            //      prompt.ShowDialog()
            //if prompt.result:
            //	self.submit_message("/connect {0} {1}".format(prompt.host, prompt.port))
        }
        public void Menu_ClearChat_Click(object sender, EventArgs e)
        {
            // self.clear_chatbox()
        }

        public void Menu_Exit_Click(object sender, EventArgs e)
        {
            // self.clear_chatbox()
        }

        public void channels_SelectionChanged(object sender, EventArgs e)
        {

            //       newName = sender.SelectedItem.Content

            //       if  self.model.currentChannel == None or newName!= self.model.currentChannel.name: #if user click diff channel change model chnl
            //		if  self.model.currentChannel == None or not self.model.channels[newName].joined: #only sendif havent joined yet
            //			self.send_command("/join " + newName)
            //		self.model.currentChannel = self.model.channels.get(newName)
            //	self.model.messages = self.model.currentChannel.messages
            //	self.model.isNewMessage = True #scroll to bottonm now
            //public void Menu_Exit_Click(self, sender, e):
            //	self.close()
        }
    }
}
