import { createContext, useContext, useState, ReactNode } from "react";
import { API_BASE_URL } from "../config/environment";

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
            // ⚡ Llamada real al backend
            console.log('🔐 Intentando login en:', `${API_BASE_URL}/users/login`);
            
            const response = await fetch(`${API_BASE_URL}/users/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ email, password }),
            });
            
            const data = await response.json();
            
            if (response.ok) {
                console.log('✅ Login exitoso:', data.user);
                setUser(data.user);
            } else {
                console.error('❌ Login fallido:', data.message);
                throw new Error(data.message || 'Login failed');
            }
        } catch (error) {
            console.error("❌ Error in login:", error);
            // En desarrollo, puedes usar un usuario fake si el backend no está disponible
            if (__DEV__) {
                console.log('⚠️ Usando usuario de desarrollo');
                const fakeUser = { id: "1", name: "Demo User", email };
                setUser(fakeUser);
            }
            throw error;
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