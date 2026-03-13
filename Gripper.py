# import time

# from pymodbus.client.sync import ModbusSerialClient


# class EPick:
#     def __init__(self, port="COM5", slave_id=9):
#         self.slave_id = slave_id
#         self.client = ModbusSerialClient(
#             method="rtu",
#             port=port,
#             baudrate=115200,
#             parity="N",
#             stopbits=1,
#             bytesize=8,
#             timeout=1
#         )

#         if not self.client.connect():
#             raise Exception("Impossible de se connecter au gripper")

#         print("Connecté au gripper")

    
#     def activate(self):
    
#         self.client.write_register(1000, 0x0900, unit=self.slave_id)
#         time.sleep(0.05)
#         print("Gripper activé")

#     def grip(self):
#         # rPR < 100 = GRIP (ex: 22 ≈ 78% vacuum)
#         self.activate()
#         self.client.write_register(1001, 22, unit=self.slave_id)
#         print("GRIP")
        
#     def release(self):
#         # rPR >= 100 = RELEASE
#         self.activate()
#         self.client.write_register(1001, 100, unit=self.slave_id)
#         print("RELEASE")
    
    
    
    
#     def status(self):
#         r2000 = self.client.read_input_registers(2000, 1, unit=self.slave_id).registers[0]
#         vacuum_state = r2000 & 0b11
#         return vacuum_state  # 0=standby, 1=grip, 2=release

#     def close(self):
#         self.client.close()
#         print("Connexion fermée")
        
    
    
# gripper = EPick("COM5")

# gripper.grip()
# time.sleep(2)

# gripper.release()
# time.sleep(2)

# gripper.close()

        





        