import { Stack } from "expo-router";
import { AvedexProvider } from "../context/avedex-context";
import { BirdDetectionProvider } from "../context/bird-detection-context";

export default function RootLayout() {
  return (
    <AvedexProvider>
      <BirdDetectionProvider>
        <Stack screenOptions={{ headerShown: false }}>
        </Stack>
      </BirdDetectionProvider>
    </AvedexProvider>
  );
}
