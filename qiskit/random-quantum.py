from qiskit import QuantumCircuit, Aer, execute
import matplotlib.pyplot as plt

def generate_random_number(num_bits):
    """
    Generates a random number with a specified number of bits using a quantum circuit.
    """
    # Create a quantum circuit with the specified number of quantum and classical bits
    qc = QuantumCircuit(num_bits, num_bits)

    # Apply a Hadamard gate to each qubit to create a superposition
    for i in range(num_bits):
        qc.h(i)

    # Measure each qubit and store the result in the corresponding classical bit
    qc.measure(range(num_bits), range(num_bits))

    print("Quantum Circuit for Random Number Generation:")
    print(qc)

    # Use the Qiskit Aer simulator to execute the circuit
    simulator = Aer.get_backend('qasm_simulator')
    # Execute the circuit once (shots=1) to get a single random outcome
    job = execute(qc, simulator, shots=1)
    result = job.result()
    counts = result.get_counts(qc)

    # The result is a dictionary where the key is the binary string
    # The binary string is read from right to left (qubit 0 is the rightmost bit)
    random_bit_string = list(counts.keys())[0]
    random_number = int(random_bit_string, 2)

    return random_number, random_bit_string

if __name__ == '__main__':
    # Specify the number of bits for the random number
    number_of_bits = 8
    random_num, random_bits = generate_random_number(number_of_bits)

    print(f"\nGenerated Random Bit String: {random_bits}")
    print(f"Generated Random Number (0-{2**number_of_bits - 1}): {random_num}")
