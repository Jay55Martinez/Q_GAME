The commit we tagged for your submission is b2b4b8ccfc1b5518d4fc40f700a3784fe0a6905b.
**If you use GitHub permalinks, they must refer to this commit or your self-eval will be rejected.**
Navigate to the URL below to create permalinks and check that the commit hash in the final permalink URL is correct:

https://github.khoury.northeastern.edu/CS4500-F23/mysterious-mongooses/tree/b2b4b8ccfc1b5518d4fc40f700a3784fe0a6905b

## Self-Evaluation Form for Milestone 4

Indicate below each bullet which method takes care of each task:

1. 'rendering the referee state' 

  - Class View: Methods: renders_board() & player_scores()
      - renders_board() : displays the pieces that are placed on the board
      https://github.khoury.northeastern.edu/CS4500-F23/mysterious-mongooses/blob/b2b4b8ccfc1b5518d4fc40f700a3784fe0a6905b/Q/Common/game_state.py#L21-L45
      - player_scores() : displays the scores of each player
      https://github.khoury.northeastern.edu/CS4500-F23/mysterious-mongooses/blob/b2b4b8ccfc1b5518d4fc40f700a3784fe0a6905b/Q/Common/game_state.py#L53-L69

2. 'scoring a placement' 

  - Class Board: Methods: num_contiguous_pieces(locations) & q_completed(locations)
      - num_contiguos_pieces(location) : calls helper method get_contiguous_pieces(locations) which scans row and column and adds all of the tiles in the row and column to get the score.
      https://github.khoury.northeastern.edu/CS4500-F23/mysterious-mongooses/blob/b2b4b8ccfc1b5518d4fc40f700a3784fe0a6905b/Q/Common/map.py#L164-L172
      - q-completed(location) : checks if a row or column is q complete. scans row using helper methods q_color_completed which determines if the group of locations provided have one piece for each possible color, and q_shape_copleted which does the same as q_color_completed but with shapes. If either q_color_completed or q_shape_completed returns true then the player receives the score for q-complete.
      https://github.khoury.northeastern.edu/CS4500-F23/mysterious-mongooses/blob/b2b4b8ccfc1b5518d4fc40f700a3784fe0a6905b/Q/Common/map.py#L204-L228

3. The 'scoring a placement' functionality clearly performs four different checks: 
  - 'length of placement'
  https://github.khoury.northeastern.edu/CS4500-F23/mysterious-mongooses/blob/b2b4b8ccfc1b5518d4fc40f700a3784fe0a6905b/Q/Common/map.py#L233-L234
  - 'bonus for finishing'
  Lines 176-177 shows the 'bonus for finishing'
  https://github.khoury.northeastern.edu/CS4500-F23/mysterious-mongooses/blob/b2b4b8ccfc1b5518d4fc40f700a3784fe0a6905b/Q/Common/game_state.py#L165-L183
  - 'segments extended along the line (row, column) of placements'
  https://github.khoury.northeastern.edu/CS4500-F23/mysterious-mongooses/blob/b2b4b8ccfc1b5518d4fc40f700a3784fe0a6905b/Q/Common/map.py#L151-L162
  - 'segments extended orthogonal to the line (row, column) of placements'
  https://github.khoury.northeastern.edu/CS4500-F23/mysterious-mongooses/blob/b2b4b8ccfc1b5518d4fc40f700a3784fe0a6905b/Q/Common/map.py#L151-L162
  - indicate which of these are factored out into separate
    methods/functions and where.
  all except 'bonus for finishing' is separated into separate methods. See the permalinks above for the location.

NOTE:
For our tests, they will not run. However, this is because we merged and submitted with an old version of shape and color enum. In the current version of code we merged the correct enums and the tests work.  
   

   
The ideal feedback for each of these points is a GitHub perma-link to
the range of lines in a specific file or a collection of files.

A lesser alternative is to specify paths to files and, if files are
longer than a laptop screen, positions within files are appropriate
responses.

You may wish to add a sentence that explains how you think the
specified code snippets answer the request.

If you did *not* realize these pieces of functionality, say so.