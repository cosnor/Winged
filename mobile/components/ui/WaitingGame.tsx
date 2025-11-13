import React, { useEffect, useRef, useState } from "react";
import { View, Text, TouchableOpacity, Animated, Dimensions, StyleSheet } from "react-native";

const { width, height } = Dimensions.get("window");
const PLAYER_SIZE = 40;
const OBSTACLE_SIZE = 40;

export default function MiniGameAvoider({ onFinish }: { onFinish: () => void }) {
  const [playerX, setPlayerX] = useState(width / 2 - PLAYER_SIZE / 2);
  const [gameOver, setGameOver] = useState(false);
  const [score, setScore] = useState(0);

  const obstacleY = useRef(new Animated.Value(0)).current;
  const [obstacleX, setObstacleX] = useState(Math.random() * (width - OBSTACLE_SIZE));

  // Movimiento del obstáculo
  const startObstacleFall = () => {
    obstacleY.setValue(0);
    Animated.timing(obstacleY, {
      toValue: height,
      duration: 2000,
      useNativeDriver: true,
    }).start(({ finished }) => {
      if (finished && !gameOver) {
        setScore((s) => s + 1);
        setObstacleX(Math.random() * (width - OBSTACLE_SIZE));
        startObstacleFall();
      }
    });
  };

  // Detección de colisión simple
  useEffect(() => {
    const interval = setInterval(() => {
      obstacleY.addListener(({ value }) => {
        const playerTop = height - 100;
        const obstacleTop = value;
        const collideX =
          playerX < obstacleX + OBSTACLE_SIZE &&
          playerX + PLAYER_SIZE > obstacleX;
        const collideY =
          playerTop < obstacleTop + OBSTACLE_SIZE &&
          playerTop + PLAYER_SIZE > obstacleTop;
        if (collideX && collideY && !gameOver) {
          setGameOver(true);
        }
      });
    }, 50);
    return () => clearInterval(interval);
  }, [playerX, obstacleX, gameOver]);

  useEffect(() => {
    startObstacleFall();
  }, []);

  const moveLeft = () => {
    if (playerX > 0) setPlayerX(playerX - 40);
  };
  const moveRight = () => {
    if (playerX < width - PLAYER_SIZE) setPlayerX(playerX + 40);
  };

  return (
    <View style={styles.container}>
      {!gameOver ? (
        <>
          <Animated.View
            style={[
              styles.obstacle,
              { transform: [{ translateY: obstacleY }], left: obstacleX },
            ]}
          />
          <View style={[styles.player, { left: playerX }]} />
          <View style={styles.controls}>
            <TouchableOpacity onPress={moveLeft} style={styles.button}>
              <Text style={styles.btnText}>⬅️</Text>
            </TouchableOpacity>
            <TouchableOpacity onPress={moveRight} style={styles.button}>
              <Text style={styles.btnText}>➡️</Text>
            </TouchableOpacity>
          </View>
          <Text style={styles.score}>Puntaje: {score}</Text>
        </>
      ) : (
        <View style={styles.gameOver}>
          <Text style={styles.gameOverText}>💥 ¡Chocaste!</Text>
          <Text style={styles.score}>Puntaje final: {score}</Text>
          <TouchableOpacity
            onPress={() => {
              setGameOver(false);
              setScore(0);
              startObstacleFall();
            }}
            style={styles.restartBtn}
          >
            <Text style={styles.btnText}>Reintentar</Text>
          </TouchableOpacity>
          <TouchableOpacity
            onPress={onFinish}
            style={[styles.restartBtn, { backgroundColor: "#444" }]}
          >
            <Text style={styles.btnText}>Salir</Text>
          </TouchableOpacity>
        </View>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#121212",
    alignItems: "center",
    justifyContent: "flex-end",
  },
  player: {
    position: "absolute",
    bottom: 60,
    width: PLAYER_SIZE,
    height: PLAYER_SIZE,
    backgroundColor: "#4CAF50",
    borderRadius: 10,
  },
  obstacle: {
    position: "absolute",
    top: 0,
    width: OBSTACLE_SIZE,
    height: OBSTACLE_SIZE,
    backgroundColor: "#F44336",
    borderRadius: 8,
  },
  controls: {
    flexDirection: "row",
    marginBottom: 20,
  },
  button: {
    marginHorizontal: 20,
    padding: 10,
    backgroundColor: "#333",
    borderRadius: 10,
  },
  btnText: {
    fontSize: 24,
    color: "#fff",
  },
  score: {
    position: "absolute",
    top: 50,
    color: "#fff",
    fontSize: 20,
  },
  gameOver: {
    alignItems: "center",
    justifyContent: "center",
  },
  gameOverText: {
    fontSize: 28,
    color: "#fff",
    marginBottom: 10,
  },
  restartBtn: {
    padding: 10,
    backgroundColor: "#2196F3",
    borderRadius: 10,
    marginTop: 10,
  },
});
