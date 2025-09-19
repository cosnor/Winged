import { createContext, useContext, useState, ReactNode } from "react";

// 1. Definir el tipo de usuario
type User = {
    id: string;
    name: string;
    email: string;
} | null;

// 2. Definir qué expone el contexto
type AuthContextType = {
    user: User;
    loading: boolean;
    login: (email: string, password: string) => Promise<void>;
    logout: () => void;
};

// 3. Crear el contexto con valores por defecto
const AuthContext = createContext<AuthContextType>({
    user: null,
    loading: false,
    login: async () => {},
    logout: () => {}
});

// 4. Proveedor del contexto
export function AuthProvider({ children }: { children: ReactNode }) {
    const [user, setUser] = useState<User>(null);
    const [loading, setLoading] = useState(false);

    const login = async (email: string, password: string) => {
        setLoading(true);
        try {
        // ⚡ Aquí iría tu lógica de login (ej: llamada API backend)
        // simulamos login
        const fakeUser = { id: "1", name: "Demo User", email };
        setUser(fakeUser);
        } catch (error) {
        console.error("Error in login:", error);
        } finally {
        setLoading(false);
        }
    };

    const logout = () => {
        setUser(null);
    };

    return (
        <AuthContext.Provider value={{ user, loading, login, logout }}>
        {children}
        </AuthContext.Provider>
    );
}

// 5. Hook para consumir el contexto
export function useAuth() {
    return useContext(AuthContext);
}