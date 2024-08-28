import chess.pgn

def find_errors(input_pgn, output_pgn, color):
    """Traverse chess moves to find strategic errors based on transpositions, considering the specified color."""

    color_to_check = chess.WHITE if color == "white" else chess.BLACK
    seen_positions = {}
    errors = []

    def traverse_game(node, board, ply=0):
        current_fen = board.fen()

        for move in node.variations:
            board.push(move.move)
            next_fen = board.fen()

            # Check for errors only when it's the specified color's turn
            if board.turn != color_to_check:
                if current_fen in seen_positions:
                    previous_moves = seen_positions[current_fen]

                    for prev_move in previous_moves:
                        # Check if the opponent responded the same way
                        if prev_move['move'].uci() != move.move.uci():
                            errors.append({
                                'error_fen': current_fen,
                                'next_fen': next_fen,
                                'error_move': move.move,
                                'expected_move': prev_move['move'],
                                'prev_game': prev_move['game'],
                                'current_game': game.headers['Event'],
                                'ply': ply + 1
                            })

            # Add the current FEN and the next move to seen_positions
            if current_fen not in seen_positions:
                seen_positions[current_fen] = []
            seen_positions[current_fen].append({
                'move': move.move,
                'game': game.headers['Event']
            })

            # Continue the recursive traversal
            traverse_game(move, board, ply + 1)
            board.pop()

    with open(input_pgn, 'r') as pgn_file:
        with open(output_pgn, 'w') as out_file:
            while True:
                game = chess.pgn.read_game(pgn_file)
                if game is None:
                    break

                board = game.board()
                traverse_game(game, board)

            # Display the detected errors
            if errors:
                out_file.write("Detected Errors:\n\n")
                for i, error in enumerate(errors):
                    board.set_fen(error['error_fen'])
                    out_file.write(f"Error {i + 1}:\n")
                    out_file.write(f"Current Game: {error['current_game']}\n")
                    out_file.write(f"Original Game: {error['prev_game']}\n")
                    out_file.write(f"Ply: {error['ply']}\n")
                    out_file.write(f"Position (before the error move):\n{board}\n")
                    out_file.write(f"Expected Move: {error['expected_move'].uci()}\n")
                    out_file.write(f"Incorrect Move: {error['error_move'].uci()}\n")
                    out_file.write("-" * 50 + "\n\n")
            else:
                out_file.write("No errors detected.\n")

    print(f"Analysis complete. Errors are saved in {output_pgn}.")
