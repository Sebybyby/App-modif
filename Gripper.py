import time
from pymodbus.client.sync import ModbusSerialClient


class EPick:
    def __init__(self, port="COM3", slave_id=9):
        self.slave_id = slave_id
        self.client = ModbusSerialClient(
            method="rtu",
            port=port,
            baudrate=115200,
            parity="N",
            stopbits=1,
            bytesize=8,
            timeout=1
        )

        if not self.client.connect():
            raise Exception("Impossible de se connecter au gripper")

        print("Connecté au gripper")

    @staticmethod
    def vacuum_percent_to_r(value_percent: int) -> int:

        value_percent = max(0, min(78, int(value_percent)))
        return 100 - value_percent

    def _write_action(self, action_byte: int):

        reg1000 = (action_byte << 8) | 0x00
        self.client.write_register(1000, reg1000, unit=self.slave_id)

    def reset(self):
        # rACT = 0 : clear faults / reset
        self._write_action(0x00)
        time.sleep(0.05)
        print("Gripper réinitialisé")

    def activate_advanced_idle(self):

        self._write_action(0x03)
        time.sleep(0.05)
        print("Gripper activé en mode avancé (idle)")

    def grip(self, vacuum_max_percent=35, vacuum_min_percent=35, timeout_s=0):
        """
        Mode avancé :
        - vacuum_max_percent : seuil max
        - vacuum_min_percent : seuil min
        - timeout_s : timeout de grip
        """
        if vacuum_min_percent > vacuum_max_percent:
            raise ValueError("vacuum_min_percent doit être <= vacuum_max_percent")

        rPR = self.vacuum_percent_to_r(vacuum_max_percent)
        rFR = self.vacuum_percent_to_r(vacuum_min_percent)
        rSP = max(0, min(255, int(round(timeout_s * 10))))  

     
        self.activate_advanced_idle()

   
        reg1001 = (0x00 << 8) | rPR


        reg1002 = (rSP << 8) | rFR

        self.client.write_register(1001, reg1001, unit=self.slave_id)
        self.client.write_register(1002, reg1002, unit=self.slave_id)


        self._write_action(0x03)  
        time.sleep(0.05)
        self._write_action(0x0B)  
        time.sleep(0.05)

        print(
            f"GRIP advanced | max={vacuum_max_percent}% (rPR={rPR}) "
            f"| min={vacuum_min_percent}% (rFR={rFR}) "
            f"| timeout={timeout_s}s (rSP={rSP})"
        )

    def release(self, release_delay_s=1.0):
        rPR = 100
        rSP = max(0, min(255, int(round(release_delay_s * 10))))
        rFR = 0

        self.activate_advanced_idle()

        reg1001 = (0x00 << 8) | rPR
        reg1002 = (rSP << 8) | rFR

        self.client.write_register(1001, reg1001, unit=self.slave_id)
        self.client.write_register(1002, reg1002, unit=self.slave_id)

        self._write_action(0x03)
        time.sleep(0.05)
        self._write_action(0x0B)
        time.sleep(0.05)

        print(f"RELEASE passif | delay={release_delay_s}s")

    def read_status(self):

        rr = self.client.read_input_registers(2000, 2, unit=self.slave_id)
        if rr.isError():
            print("Erreur lecture status")
            return None

        reg2000, reg2001 = rr.registers

        gPR = reg2001 & 0x00FF
        gPO = (reg2001 >> 8) & 0x00FF

        print(
            f"Status raw: 2000=0x{reg2000:04X}, 2001=0x{reg2001:04X} | "
            f"gPR={gPR}, gPO={gPO}"
        )
        return reg2000, reg2001, gPR, gPO

    def close(self):
        self.client.close()
        print("Connexion fermée")


if __name__ == "__main__":
    gripper = EPick(port="COM3", slave_id=9)

    try:
        gripper.reset()
        time.sleep(0.2)

        gripper.grip(vacuum_max_percent=35, vacuum_min_percent=20, timeout_s=3.0)
        time.sleep(0.5)
        gripper.read_status()

        time.sleep(2)

        gripper.release(release_delay_s=1.0)
        time.sleep(0.5)
        gripper.read_status()

    finally:
        gripper.close()