import chess.pgn
import os

def optimize(input_pgn, output_pgn):
    """Optimize a PGN file by removing duplicate sequences and adding FEN headers."""
    
    # List to store seen FENs
    seen_fens = []        

    # Open the input PGN file
    with open(input_pgn, 'r') as pgn_file:
        # Prepare to write to the output PGN file
        with open(output_pgn, 'w') as out_file:
            while True:
                # Read the next game from the PGN file
                game = chess.pgn.read_game(pgn_file)
                if game is None:
                    break
                
                board = game.board()
                starting_fen = None

                def find_starting_node(node, board, has_duplicate=False, is_mainline=True):
                    nonlocal starting_fen
                    # Find the starting node recursively
                    variations = node.variations
                    for variation in variations:
                        board.push(variation.move)
                        fen = board.fen()

                        # Check if the FEN has already been seen
                        fen_exist = next((t for t in seen_fens if t['fen'] == fen), None)

                        if fen_exist:
                            if is_mainline:
                                has_duplicate = True
                        else:
                            if has_duplicate:
                                is_mainline = False
                            seen_fens.append({
                                'fen': fen,
                                'original_game': game,
                                'move': variation
                            })

                        if is_mainline:
                            starting_fen = fen
                        else:
                            # Add the next node for the next game
                            result = find_starting_node(variation, board, has_duplicate, is_mainline)
                            board.pop()
                            return variation
                        
                        result = find_starting_node(variation, board, has_duplicate, is_mainline)
                        board.pop()
                        return result
                        
                starting_node = find_starting_node(game, board)


                # # Update the name here for consistency
                # opening = game.headers.get('Opening', '?')
                # first_move = starting_node if starting_node else game.variations[0] if game.variations else None
                # options = len(game.variations) > 1 if game.variations else False
                # first_move_san = first_move.san() if first_move else ''
                # first_move_ply = first_move.ply() if first_move else 0
                # move_number = (first_move_ply + 1) // 2  # Calculer le numéro de coup
                # if first_move_ply % 2 == 1:  # Si le numéro de coup est impair
                #     move_string = f"{move_number}."
                # else:  # Si le numéro de coup est pair
                #     move_string = f"{move_number}..."


                # print(game, first_move_san)
                # if opening != "?":
                #     game.headers['Event'] = f"{opening}"
                #     if options:
                #         game.headers['Event'] += f" - {move_string} Options"
                #     elif first_move_san:
                #         game.headers['Event'] += f" - ({move_string}{first_move_san})"

                # Check if starting node is not the root node. If it is, do nothing.
                if starting_node is None or starting_fen is None:
                    exporter = chess.pgn.StringExporter(headers=True, variations=True, comments=True)
                    out_file.write(game.accept(exporter) + "\n\n")
                    continue
                
                print(f"Optimizing {game.headers['Event']}...")

                new_game = chess.pgn.Game()
                new_game.headers = game.headers
                
                new_game.setup(starting_fen)
                new_game.variations = starting_node.parent

                # Add the starting node to the new game
                exporter = chess.pgn.StringExporter(headers=True, variations=True, comments=True)
                out_file.write(new_game.accept(exporter) + "\n\n")
                
    print(f"Optimization complete. Output saved to {output_pgn}.")
