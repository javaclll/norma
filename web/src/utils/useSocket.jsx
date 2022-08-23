import { useState, useEffect, useRef } from "react";

const useSocket = ({
  onConnect = null,
  fire = true,
  close = false,
  onMessage,
  websock_host,
}) => {
  const [isReady, setIsReady] = useState(false);
  const [history, setHistory] = useState([]);
  const [closeState, setCloseState] = useState(close);
  const ws = useRef(null);

  useEffect(() => {
    if (fire) {
      ws.current = new WebSocket(`${websock_host}`);
      if (!onConnect) {
        ws.current.onopen = () => {
          setIsReady(true);
        };
      } else {
        ws.current.onopen = (data) => {
          setIsReady(true);
          onConnect(data);
        };
      }
    }
  }, [fire]);

  useEffect(() => {
    if (fire && isReady) {
      ws.current.onmessage = (data) => {
        let ret = onMessage(data);
        if (ret) {
          if (ret.multi) {
            setHistory([...history, ...ret.data]);
          } else {
            setHistory([...history, ret.data]);
          }
        }
      };
    }
  }, [fire, onMessage, onConnect, isReady]);

  useEffect(() => {
    if (close && ws.current) {
      ws.current.close();
    }
  }, [closeState, setCloseState]);
  return [ws.current, history, isReady, setCloseState];
};
export default useSocket;
