import { Stack } from "expo-router";
import { AvedexProvider } from "../context/avedex-context";

export default function RootLayout() {
  return (
    <AvedexProvider>
      <Stack>
        <Stack.Screen name="index" options={{ headerShown: false }} />
        <Stack.Screen name="(auth)" options={{ headerShown: false }} />
        <Stack.Screen name="(app)" options={{ headerShown: false }} />
      </Stack>
    </AvedexProvider>
  );
}
