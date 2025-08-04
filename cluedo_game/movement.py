"""
Movement module for the Cluedo game.
Handles movement logic for both human and AI players using BFS algorithm.
"""
from collections import deque
from typing import List, Dict, Any, Set, Tuple, Union, Optional


class Movement:
    def __init__(self, mansion):
        """
        Initialize the Movement class.
        
        Args:
            mansion: The Mansion object containing rooms, corridors, and adjacency map
        """
        self.mansion = mansion
        self._secret_passage_rooms = {
            'Kitchen', 'Study', 'Conservatory', 'Lounge'
        }

    def _is_secret_passage_move(self, from_pos, to_pos):
        """
        Check if moving from one position to another uses a secret passage.
        
        Args:
            from_pos: Starting position (Room or corridor)
            to_pos: Destination position (Room or corridor)
            
        Returns:
            bool: True if this move uses a secret passage, False otherwise
        """
        # If either position is a corridor, it's not a secret passage move
        if (isinstance(from_pos, str) and from_pos.startswith('C')) or \
           (isinstance(to_pos, str) and to_pos.startswith('C')):
            return False
            
        # If either position isn't a room (after checking for corridors), it's not a secret passage
        if not hasattr(from_pos, 'name') or not hasattr(to_pos, 'name'):
            return False
            
        # Get room names
        from_room = from_pos.name
        to_room = to_pos.name
        
        # Check for secret passage pairs
        return ((from_room in ['Kitchen', 'Study'] and to_room in ['Kitchen', 'Study']) or
                (from_room in ['Conservatory', 'Lounge'] and to_room in ['Conservatory', 'Lounge']))

    def get_destinations_from(self, start_position: Union[str, Any], steps: int) -> List[str]:
        """
        Find all possible destinations that can be reached from a starting position 
        within a given number of steps using BFS (Breadth-First Search).
        
        Args:
            start_position: The starting position (room or corridor)
            steps: Number of steps (dice roll) available to the player
            
        Returns:
            A list of possible destination spaces sorted alphabetically
        """
        if steps <= 0:
            return []
            
        # Convert string room names to Room objects
        if isinstance(start_position, str) and not start_position.startswith('C'):
            for room in self.mansion.rooms:
                if room.name == start_position:
                    start_position = room
                    break
        
        # Track visited positions with their distances and secret passage usage
        visited = {}  # (position_key, used_secret_passage) -> distance
        queue = deque([(start_position, 0, False)])  # (position, distance, used_secret_passage)
        reachable = set()  # (position_key, used_secret_passage)
        
        def get_position_key(pos) -> str:
            """Helper to get a consistent key for any position type."""
            return pos if isinstance(pos, str) else getattr(pos, 'name', str(pos))
            
        start_key = get_position_key(start_position)
        visited[(start_key, False)] = 0
        
        while queue:
            pos, dist, used_secret_passage = queue.popleft()
            pos_key = get_position_key(pos)
            
            # Add as a valid destination if it's not the starting position
            if dist > 0:
                reachable.add((pos_key, used_secret_passage))
            
            # Don't explore beyond the current position if we've used all steps
            if dist >= steps:
                continue
                
            # Explore adjacent spaces
            for adj in self.mansion.get_adjacent_spaces(pos):
                adj_key = get_position_key(adj)
                
                # Check if this move uses a secret passage
                is_secret_passage = self._is_secret_passage_move(pos, adj)
                
                # If we've already used a secret passage and this is another one, skip it
                new_used_secret_passage = used_secret_passage or is_secret_passage
                
                # Skip if already visited with same or fewer steps and same or better secret passage usage
                if (adj_key, new_used_secret_passage) in visited and \
                   visited[(adj_key, new_used_secret_passage)] <= dist + 1:
                    continue
                    
                # All moves cost 1 step
                new_dist = dist + 1
                
                # If this move would exceed our step limit, skip it
                if new_dist > steps:
                    continue
                    
                visited[(adj_key, new_used_secret_passage)] = new_dist
                queue.append((adj, new_dist, new_used_secret_passage))
                
        # Convert reachable set to a sorted list of position strings
        final_destinations = set()
        for pos_key, used_secret_passage in reachable:
            # For display, add a note if a secret passage was used to get here
            display_name = f"{pos_key} (via secret passage)" if used_secret_passage else pos_key
            final_destinations.add(display_name)
                
        return sorted(final_destinations, key=str)
    
    def display_board(self) -> None:
        """Display the board layout with chess coordinates."""
        if not hasattr(self.mansion, 'chess_coordinates'):
            print("\nBoard display not available: no chess coordinates found.")
            return
            
        output = []
        
        # Add rooms section
        output.append("Rooms:")
        
        # Get all rooms and sort them by their coordinates
        rooms_with_coords = []
        for room in self.mansion.rooms:
            room_name = room.name
            if room_name in self.mansion.chess_coordinates:
                coord = self.mansion.chess_coordinates[room_name]
                rooms_with_coords.append((room_name, coord))
        
        # Sort by number then letter (e.g., A1, A3, C1, etc.)
        rooms_with_coords.sort(key=lambda x: (x[1][1], x[1][0]))
        
        for room_name, coord in rooms_with_coords:
            output.append(f"- {room_name} ({coord})")
        
        # Add corridors section
        output.append("\nCorridors:")
        
        # Get all corridors and sort them
        corridors_with_coords = []
        for corridor in [f"C{i}" for i in range(1, 13)]:
            if corridor in self.mansion.chess_coordinates:
                coord = self.mansion.chess_coordinates[corridor]
                corridors_with_coords.append((corridor, coord))
        
        # Sort by number then letter
        corridors_with_coords.sort(key=lambda x: (x[1][1], x[1][0]))
        
        for corridor, coord in corridors_with_coords:
            output.append(f"- {corridor} ({coord})")
        
        # Add secret passages section
        output.append("\nSecret Passages:")
        output.append("- Kitchen <-> Study")
        output.append("- Conservatory <-> Lounge")
        
        # Print the output
        full_output = '\n'.join(output)
        if hasattr(self.mansion, 'output'):
            self.mansion.output(full_output)
        else:
            print(full_output)
    
    def get_optimal_path(self, start_position, end_position, max_steps=None):
        """
        Find the optimal (shortest) path between two positions using BFS.
        
        Args:
            start_position: The starting position (can be a Room, Corridor, or string name)
            end_position: The target position (can be a Room, Corridor, or string name)
            max_steps: Maximum number of steps allowed (optional)
                
        Returns:
            A list of positions representing the path (excluding start), or [] if no path exists
        """
        # Handle case where we're already at the destination
        if start_position == end_position:
            return []
            
        # Get string names for positions for comparison
        start_name = getattr(start_position, 'name', start_position)
        end_name = getattr(end_position, 'name', end_position)
        
        # Check for direct secret passage if start and end are connected by one
        if self._is_secret_passage_move(start_position, end_position):
            return [end_position]
            
        # Get adjacent spaces from the starting position
        adj_spaces = self.mansion.get_adjacent_spaces(start_position)
        
        # If there are no adjacent spaces, path is impossible
        if not adj_spaces:
            return []
                
        # Check if end is directly adjacent to start
        for adj in adj_spaces:
            adj_name = getattr(adj, 'name', adj)
            if adj_name == end_name or adj == end_position:
                return [adj]
            
        # If max_steps is 1 or less, and we haven't found a direct path, return empty
        if max_steps is not None and max_steps <= 1:
            return []
                
        # For longer paths, use BFS
        from collections import deque
            
        # Queue items are (current_position, path_taken, steps_used, used_secret_passage)
        queue = deque()
        visited = set()
        
        # Start with all adjacent positions from the starting position
        for adj in adj_spaces:
            # Check if this is a secret passage move
            is_secret_passage = self._is_secret_passage_move(start_position, adj)
            
            # Add to queue with initial path and secret passage usage
            queue.append((adj, [adj], 1, is_secret_passage))
            
            # Mark as visited with current secret passage state
            adj_key = adj if isinstance(adj, str) else getattr(adj, 'name', str(adj))
            visited.add((adj_key, is_secret_passage))
        
        while queue:
            current, path, steps_used, used_secret_passage = queue.popleft()
            current_key = current if isinstance(current, str) else getattr(current, 'name', str(current))
            
            # Check if we've reached the end
            if current == end_position:
                return path
                
            # Don't explore further if we've used all our steps
            if max_steps is not None and steps_used >= max_steps:
                continue
                
            # Explore adjacent positions
            for adj in self.mansion.get_adjacent_spaces(current):
                adj_key = adj if isinstance(adj, str) else getattr(adj, 'name', str(adj))
                
                # Check if this is a secret passage move
                is_secret_passage_move = self._is_secret_passage_move(current, adj)
                
                # If we've already used a secret passage and this is another one, skip it
                new_used_secret_passage = used_secret_passage or is_secret_passage_move
                
                # Skip if we've already visited this position with the same or better secret passage usage
                if (adj_key, new_used_secret_passage) in visited:
                    continue
                    
                # Add to visited and queue
                visited.add((adj_key, new_used_secret_passage))
                queue.append((adj, path + [adj], steps_used + 1, new_used_secret_passage))
        
        # If we get here, no path was found
        return []

    def is_path_possible(self, start_position, end_position, max_steps):
        """
        Check if a path exists between two positions within a given number of steps.
        
        Args:
            start_position: The starting position
            end_position: The target position
            max_steps: Maximum number of steps allowed
            
        Returns:
            bool: True if a path exists within max_steps, False otherwise
        """
        path = self.get_optimal_path(start_position, end_position, max_steps)
        return len(path) > 0

    def get_neighboring_rooms(self, position, include_corridors=False):
        """
        Get all neighboring rooms (and optionally corridors) from a position.
        
        Args:
            position: The current position
            include_corridors: Whether to include corridors in the result
            
        Returns:
            List of neighboring rooms (and possibly corridors). 
            If include_corridors is True, returns corridor names as strings.
        """
        if include_corridors:
            # Get adjacent spaces and convert any corridor objects to their string names
            adjacent = self.mansion.get_adjacent_spaces(position)
            return [getattr(space, 'name', space) for space in adjacent]
        else:
            return self.mansion.get_adjacent_rooms(position)
            
    def find_closest_room(self, position, room_filter=None):
        """
        Find the closest room from the current position.
        
        Args:
            position: The current position
            room_filter: Optional function to filter which rooms to consider
            
        Returns:
            The closest room and distance to it as (room, distance) tuple
        """
        all_rooms = self.mansion.get_rooms()
        
        # Apply filter if provided
        if room_filter:
            target_rooms = [r for r in all_rooms if room_filter(r)]
        else:
            target_rooms = all_rooms
            
        # Check if the current position is already a room and matches the filter
        if position in target_rooms:
            return (position, 0)
            
        # Convert position to a string key if it's a Room object
        pos_key = getattr(position, 'name', position)
            
        # Find the closest room using BFS
        visited = set([pos_key])
        queue = deque([(position, 0)])  # (position, distance)
        
        while queue:
            pos, dist = queue.popleft()
            
            # Check if it's a target room
            if pos in target_rooms:
                return (pos, dist)
                
            # Explore adjacent spaces
            for adj in self.mansion.get_adjacent_spaces(pos):
                adj_key = getattr(adj, 'name', adj)
                if adj_key not in visited:
                    visited.add(adj_key)
                    queue.append((adj, dist + 1))
                    
        # No room found
        return (None, float('inf'))
