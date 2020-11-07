/*
 Navicat Premium Data Transfer

 Source Server         : 192.168.0.226
 Source Server Type    : MariaDB
 Source Server Version : 100147
 Source Host           : 192.168.0.226:3306
 Source Schema         : examination

 Target Server Type    : MariaDB
 Target Server Version : 100147
 File Encoding         : 65001

 Date: 07/11/2020 13:46:50
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for contact
-- ----------------------------
DROP TABLE IF EXISTS `contact`;
CREATE TABLE `contact`  (
  `user_id` int(11) NOT NULL,
  `email` varchar(30) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `mobile` varchar(20) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `is_delete` tinyint(1) NOT NULL DEFAULT 0,
  PRIMARY KEY (`user_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Compact;

SET FOREIGN_KEY_CHECKS = 1;
