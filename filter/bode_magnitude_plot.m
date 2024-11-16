pkg load control; % Load the Control Systems Toolbox

% Define the numerator and denominator of the transfer function
num = [1, 75 + 211, 75 * 211]; % Coefficients of (s + 75)(s + 211)
den = [1, 84 + 188, 84 * 188]; % Coefficients of (s + 84)(s + 188)

% Create the transfer function
T = tf(num, den);

% Define frequency range for the plot (in radians/second)
w = logspace(-1, 3, 500); % Frequencies from 10^-1 to 10^3

% Calculate the magnitude of the frequency response
[mag, ~] = bode(T, w);

% Convert magnitude to dB
mag_dB = 20 * log10(mag(:));

% Plot the magnitude in dB vs frequency
semilogx(w, mag_dB);
grid on;
xlabel('Frequency (rad/s)');
ylabel('Magnitude (dB)');
title('Bode Magnitude Plot');
