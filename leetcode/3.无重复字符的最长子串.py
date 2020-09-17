#
# @lc app=leetcode.cn id=3 lang=python3
#
# [3] 无重复字符的最长子串
#

# @lc code=start
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        str_dict = {}
        len_max, str_index = 0, -1
        for i, n in enumerate(s):
            if n in str_dict and str_dict[n] > str_index:
                str_index = str_dict[n]
                str_dict[n] = i
            else:
                str_dict[n] = i
                len_max = max(len_max, i - str_index)
        return len_max
# @lc code=end

