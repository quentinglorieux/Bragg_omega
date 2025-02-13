from pyrpl import Pyrpl


# Methods:
# connect() - Establishes a connection to the Red Pitaya.
# set_trigger_pulse(high_level: float, low_level: float, period: float, duty_cycle: float) - Configures a pulse train on Channel 1.
# set_dc_voltage(voltage: float) - Sets a DC voltage on Channel 2 for frequency control.
# disable_outputs() - Turns off both signal generator outputs.
# disconnect() - Closes the connection to Red Pitaya.


class RedPitayaSignalGenerator:
    """
    Driver for the Red Pitaya used as a 2-channel signal generator.
    - Channel 1: Pulse train for triggering.
    - Channel 2: DC voltage for frequency control.
    """

    def __init__(self, ip: str = "192.168.1.100"):
        """
        Initializes the Red Pitaya Signal Generator.

        Args:
            ip (str): IP address of the Red Pitaya.
        """
        self.ip = ip
        self.pyrpl = None

    def connect(self):
        """Establishes a connection to Red Pitaya."""
        try:
            self.pyrpl = Pyrpl(hostname=self.ip)
            print(f"Connected to Red Pitaya at {self.ip}")
        except Exception as e:
            print(f"Error connecting to Red Pitaya: {e}")

    def set_trigger_pulse(self, high_level: float, low_level: float, period: float, duty_cycle: float):
        """
        Configures a pulse train on Channel 1.

        Args:
            high_level (float): Voltage for HIGH state (V).
            low_level (float): Voltage for LOW state (V).
            period (float): Total period of the pulse in seconds.
            duty_cycle (float): Duty cycle percentage (0-100%).
        """
        if self.pyrpl:
            asg = self.pyrpl.rp.asg0  # Access ASG0 (Channel 1)
            
            # Ensure valid input values
            if not (0 <= duty_cycle <= 100):
                print("Invalid duty cycle! Must be between 0% and 100%.")
                return

            if period <= 0:
                print("Invalid period! Must be greater than 0.")
                return
            
            # Calculate frequency
            frequency = 1 / period

            # Calculate amplitude & offset
            amplitude = (high_level - low_level) / 2
            offset = (high_level + low_level) / 2

            asg.setup(
                waveform="square",
                frequency=frequency,
                amplitude=amplitude,
                offset=offset,
                trigger_source="immediately",
            )
            print(f"Pulse set: High {high_level}V, Low {low_level}V, Period {period}s, Duty {duty_cycle}%")

    def set_dc_voltage(self, voltage: float):
        """
        Sets a DC voltage on Channel 2 for frequency control.

        Args:
            voltage (float): Voltage in Volts (0V to 1.8V).
        """
        if self.pyrpl:
            asg = self.pyrpl.rp.asg1  # Access ASG1 (Channel 2)

            # 0V - 1.8V range
            voltage = max(0, min(1.8, voltage))
            
            asg.setup(
                waveform="dc",
                offset=voltage,
            )
            print(f"DC output set to {voltage} V")

    def disable_outputs(self):
        """Turns off both signal generator outputs."""
        if self.pyrpl:
            self.pyrpl.rp.asg0.output_direct = "off"
            self.pyrpl.rp.asg1.output_direct = "off"
            print("Outputs disabled.")

    def disconnect(self):
        """Closes the connection to Red Pitaya."""
        if self.pyrpl:
            print("Red Pitaya disconnected.")
            self.pyrpl = None