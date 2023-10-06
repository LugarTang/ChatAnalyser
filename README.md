# ChatAnalyser

This tool is used to calculate some indices from WeChat chat log.

## Method

Considering that people are inclined to send many messages at one time instead of separating them by commas, we join all messages whose time interval is within a given argument `longest_pause`.

## Indices

1. Average response time.
2. Average response length.
3. Pure non-text reply frequency, which indicates how often a user wanted to end this conversation.

## Usage

1. Choose the conversation you want to analyse in WeChat and export it as emails.

   You'll get a log like this:(Empty line deleted. You don't need to do that.)

   ```
   y 17:06
   我不喜欢看
   m 17:09
   行 你也代入不进去
   m 17:09
   人家都是什么五院四系教授宠儿
   m 17:10
   [表情]
   y 17:14
   [表情]
   m 17:17
   感谢你给了我一个用指标量化聊天的想法 等我实现出来 一定能把你和我的聊天归类到最次一等
   m 17:17
   [表情]
   y 17:20
   太深奥了
   m 17:21
   你等着吧 晚上我就写出来
   ```
2. Copy that into `conversation.txt` in the same directory of `chatanalyser.py`.
3. Run `chatanalyser.py`.
4. The result will be in `output.txt`.
