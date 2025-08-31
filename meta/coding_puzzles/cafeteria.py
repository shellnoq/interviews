from typing import List

def getMaxAdditionalDinersCount(N: int, K: int, M: int, S: List[int]) -> int:
  """
  Compute the maximum number of additional diners that can be seated on a row of N seats
  while keeping at least K empty seats to the left and right of every occupied seat.

  Parameters
  ----------
  N : total number of seats (1..N)
  K : required empty-seat buffer on each side of any occupied seat
  M : number of currently occupied seats
  S : positions (1-indexed) of the currently occupied seats; no two violate distancing

  Approach
  --------
  - Sort the occupied seats.
  - Turn the row into disjoint "free segments" after removing the K-seat exclusion
    zones around each occupied seat.
      * Left edge:    L = S[0] - K - 1
      * Between i,i+1 L = (S[i+1] - S[i] - 1) - 2K
      * Right edge:   L = N - (S[-1] + K)
  - In any free segment of length L, the maximum number of new diners is:
        floor((L + K) / (K + 1))
    Rationale: each diner consumes 1 seat plus K buffer seats; at the segment’s end,
    no trailing buffer is needed, which is captured by the "+K" in the numerator.

  Time:  O(M log M) due to sorting. Works for very large N (Python ints are unbounded).
  """
  if M == 0:
    # Single free segment: the whole row
    return (N + K) // (K + 1)

  S.sort()
  additional_diners = 0

  # prev_blocked_right is the right edge (inclusive) of the last blocked zone
  # we've processed. Start with 0 meaning "no seats blocked yet".
  prev_blocked_right = 0

  # Process the free segment before each existing diner
  for pos in S:
    # Current free segment boundaries after the previous blocked zone
    start = prev_blocked_right + 1
    # We must stop at (pos - K - 1) to keep K empty seats before `pos`
    end = pos - K - 1

    if end >= start:
      L = end - start + 1
      additional_diners += (L + K) // (K + 1)

    # Update the right edge of the blocked zone created by this diner
    prev_blocked_right = pos + K

  # Finally process the free segment after the last existing diner
  start = prev_blocked_right + 1
  end = N
  if end >= start:
    L = end - start + 1
    additional_diners += (L + K) // (K + 1)

  return additional_diners

# Example test cases
assert getMaxAdditionalDinersCount(10, 1, 2, [2, 6]) == 3
assert getMaxAdditionalDinersCount(15, 2, 3, [11, 6, 14]) == 1