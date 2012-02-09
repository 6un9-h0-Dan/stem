"""
Classes for interacting with the tor control socket.

Controllers are a wrapper around a ControlSocket, retaining its low-level
connection methods (send, recv, is_alive, etc) in addition to providing methods
for interacting at a higher level.

from_port - Provides a Controller based on a port connection.
from_socket_file - Provides a Controller based on a socket file connection.

BaseController - ControlSocket subclass providing asynchronous message handling.
"""

import stem.socket

class BaseController(stem.socket.ControlSocket):
  """
  Controller for the tor process. This is a minimal base class for other
  controllers, providing basic process communication and event listing. Don't
  use this directly - subclasses provide higher level functionality.
  
  Do not continue to directly interacte with the ControlSocket we're
  constructed from - use our wrapper methods instead.
  """
  
  # TODO: Convenience methods for the BaseController are pointless since
  # callers generally won't want to make instances of this directly. Move
  # these to the Controller class once we have one.
  
  def from_port(control_addr = "127.0.0.1", control_port = 9051):
    """
    Constructs a ControlPort based Controller.
    
    Arguments:
      control_addr (str) - ip address of the controller
      control_port (int) - port number of the controller
    
    Returns:
      stem.control.Controller attached to the given port
    
    Raises:
      stem.socket.SocketError if we're unable to establish a connection
    """
    
    control_port = stem.socket.ControlPort(control_addr, control_port)
    return BaseController(control_port)
  
  def from_socket_file(socket_path = "/var/run/tor/control"):
    """
    Constructs a ControlSocketFile based Controller.
    
    Arguments:
      socket_path (str) - path where the control socket is located
    
    Returns:
      stem.control.Controller attached to the given socket file
    
    Raises:
      stem.socket.SocketError if we're unable to establish a connection
    """
    
    control_socket = stem.socket.ControlSocketFile(socket_path)
    return BaseController(control_socket)
    
  from_port = staticmethod(from_port)
  from_socket_file = staticmethod(from_socket_file)
  
  def __init__(self, control_socket):
    self._socket = control_socket
    
    def provide_self(): return self
    self._socket._get_self = provide_self
  
  def send(self, message, raw = False):
    self._socket.send(message, raw)
  
  def recv(self):
    return self._socket.recv()
  
  def is_alive(self):
    return self._socket.is_alive()
  
  def connect(self):
    self._socket.connect()
  
  def close(self):
    self._socket.close()
  
  def get_socket(self):
    return self._socket
  
  def add_status_listener(self, callback, spawn = True):
    self._socket.add_status_listener(callback, spawn)
  
  def remove_status_listener(self, callback):
    self._socket.remove_status_listener(callback)
  
  def _make_socket(self):
    self._control_socket._make_socket()

