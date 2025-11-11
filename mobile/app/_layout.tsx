import { Stack } from "expo-router";
import { AvedexProvider } from "../context/avedex-context";

export default function RootLayout() {
  return (
    <AvedexProvider>
      <Stack screenOptions={{ headerShown: false }}>
      </Stack>
    </AvedexProvider>
  );
}
