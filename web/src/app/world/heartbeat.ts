import { heartbeat } from "@/architextSDK";
import { useEffect } from "react";
import { Socket } from "socket.io-client";

function useHeartbeat(socket: Socket, seconds_interval: number = 20) {
  useEffect(() => {
    if (!socket) return;

    // Función para enviar el heartbeat
    const sendHeartbeat = async () => {
      await heartbeat(socket, {});
    };

    sendHeartbeat();
    const interval = setInterval(sendHeartbeat, 1000*seconds_interval);

    return () => clearInterval(interval);
  }, [socket, seconds_interval]);
}

export default useHeartbeat;
