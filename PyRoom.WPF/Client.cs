using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Sockets;
using System.Text;
using System.Threading.Tasks;

namespace PyRoom.WPF
{
    class Client
    {
        public bool IsClientConnected { get; set; } = false;
        public Socket socket;

        public async Task Connect(string Host, int Port = 50000)
        {

            try
            {
                socket = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
                var fac = new TaskFactory();
                await fac.FromAsync(socket.BeginConnect(Host, Port, (a) => { }, null), async (a) => {
                    IsClientConnected = true;
                    socket.EndConnect(a);
                });

            }
            catch
            {
            //    if errorMessage.errno == socket.error.errno:
            //    sys.stderr.write('Connection refused to ' + str(host) + ' on port ' + str(port))
            //else:
            //    sys.stderr.write('Failed to create a client socket: Error - %s\n', errorMessage[1])
            }
        }
         
        public void Disconnect()
        {
            if (IsClientConnected)
            {
                socket.Close();
                IsClientConnected = false;
            }
        }

        public void Send(string Data)
        {
            if (!IsClientConnected)
                return;

            socket.Send(new byte[] { });
        }
         public string Receive()
        {
            if (!IsClientConnected)
                return "";

            //socket.Receive(null);

            return "";
        }
    }
}
