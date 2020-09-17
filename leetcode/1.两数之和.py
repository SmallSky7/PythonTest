#
# @lc app=leetcode.cn id=1 lang=python3
#
# [1] 两数之和
#

# @lc code=start
class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        target_index = []
        for i in range(0, len(nums)):
            target_num = target - nums[i]
            for j in range(i+1, len(nums)):
                if nums[j] == target_num:
                    target_index.append(i)
                    target_index.append(j)
        return target_index
# @lc code=end

