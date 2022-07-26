# Message Format Specification

## HTTP Endpoint
#### Generate a new session
Endpoint: `/session`

Method: `POST`

Payload: `None`

Response:
```
{
  "success": True,
  "ident": "d9d8a955-811a-465e-8487-bbb9ccd79073",
}
```

#### Create a new game
Endpoint: `/create-game`

Method: `POST`

Payload:
```
{
  "preference": -1 | 1,
}
```

Response:
```
{
  "success": True,
  "piece": -1 | 1,
  "game_id": "c6f031b8-8f75-4869-b1f7-aff64cf88865",
}
```

## Websocket Endpoint
Endpoint: `/game/{game_id}?ident={ident}`

### Websocket Requests
#### Make a Move
Description: Make a move on the board.

Payload:
```
{
  "type": 1,
  "move": "A1B1",
}
```

Expected Response Type: `5 (Player Move Broadcast)` or `4 (Error Notification Broadcast)`

#### Resign
Payload:
```
{
  "type": 2,
}
```

#### Load Game
Payload:
```
{
  "type": 3,
  "pgn": "XXA3 - A1A2 - XXA4 - A5B5 - XXA5 - B5C5 - XXB5"
}
```

### Websocket Responses
#### Notification Broadcast
```
{
  "type": 4,
  "message": "Unauthorized user!"
}
```

#### Player Move Broadcast
```
{
  "type": 5,
  "move": "XXA3"
}
```

#### Win/Loss Broadcast
```
{
  "type": 6,
  "won_by": -1 | 1,
  "reason": "resign" | "normal",
}
```

#### Game State Broadcast
```
{
  "type": 7,
  "pgn": "XXA3 - A1A2 - XXA4 - A5B5 - XXA5 - B5C5 - XXB5"
}
```

#### Piece Assign Notification
```
{
  "type": 8,
  "piece": -1 | 1,
}
```
