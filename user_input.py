class UserInput:
    def input_values(self):
        number_storeys = int(input("Enter the number of storeys: "))

        storey_masses = []
        eigenvalues = []
        i = 0
        while i < number_storeys:
            i = i + 1
            storey_masses.append(
                float(input("Enter the mass of storey #" + str(i) + " [ton]: "))
            )
        print("\n")
        n = 0
        while n < number_storeys:
            n = n + 1
            eigenvalues.append(float(input("Enter the eigenvalues #" + str(n) + ": ")))
        print("\n")
        # 3rd x coordinate of bilinear curve
        dp = float(input("Enter the value of d*p [m]: "))

        μ_DB = float(input("\nEnter the value of μ(DB): "))
        k_DB = float(input("\nEnter the value of k(DB): "))
        Kf = float(input("\nEnter the value of K(F): "))

        data = [storey_masses, eigenvalues, dp, μ_DB, k_DB, Kf]
        return data

    # TODO:Create a funtion to sanitize the input
