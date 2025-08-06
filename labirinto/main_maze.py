import time
from maze import Maze
from collections import deque

def dfs_stack(maze: Maze, start_pos):
    stack = deque()
    visited = set()
    stack.append((start_pos, [start_pos]))

    while stack:
        current_pos, path = stack.pop()
        x, y = current_pos

        if current_pos in visited:
            continue
        visited.add(current_pos)

        if maze.find_prize(current_pos):
            print("🎉 Prêmio encontrado!")
            for step in path:
                maze.mov_player(step)
                time.sleep(0.05)
            return True

        maze.mov_player(current_pos)
        time.sleep(0.02)

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_pos = (x + dx, y + dy)
            if maze.is_free(new_pos) and new_pos not in visited:
                stack.append((new_pos, path + [new_pos]))

    print(" Prêmio não encontrado.")
    return False

# --- EXECUÇÃO PRINCIPAL ---
if __name__ == "__main__":
    maze = Maze()
    maze.load_from_csv("labirinto1.txt")
    maze.run()
    maze.init_player()
    start = maze.get_init_pos_player()
    dfs_stack(maze, start)
