# def find_microstructure_profiles(P, W, P_min, W_min, direction, min_duration, fs):
#     """
#     Extract indices where an instrument is moving up or down (profile segments).

#     Parameters
#     ----------
#     P : array_like
#         Pressure vector.
#     W : array_like
#         Rate-of-change of pressure (same length as P).
#     P_min : float
#         Minimum pressure for a valid profile.
#     W_min : float
#         Minimum magnitude of rate-of-change for a valid profile.
#     direction : str
#         'up' or 'down' (direction of profile).
#     min_duration : float
#         Minimum duration for a valid profile [seconds].
#     fs : float
#         Sampling rate in samples per second.

#     Returns
#     -------
#     profile : np.ndarray, shape (2, N)
#         Each column contains the start and end indices of a profile.
#         Empty if no profiles detected.
#     """
#     min_samples = int(np.round(min_duration * fs))
#     W = np.asarray(W)
#     P = np.asarray(P)

#     if direction.lower() == 'up':
#         W = -W

#     n = np.where((P > P_min) & (W >= W_min))[0]
#     if len(n) < min_samples:
#         return np.empty((2, 0), dtype=int)

#     diff_n = np.diff(n, prepend=n[0])
#     m = np.where(diff_n > 1)[0]
#     m = m[m != 1]

#     if len(m) == 0:
#         profile = np.array([[n[0]], [n[-1]]])
#     else:
#         profile = np.zeros((2, len(m) + 1), dtype=int)
#         profile[:, 0] = [n[0], n[m[0] - 1]]
#         for idx in range(1, len(m)):
#             profile[:, idx] = [n[m[idx - 1]], n[m[idx] - 1]]
#         profile[:, -1] = [n[m[-1]], n[-1]]

#     profile_length = profile[1, :] - profile[0, :]
#     mm = np.where(profile_length >= min_samples)[0]
#     profile = profile[:, mm]
#     return profile
