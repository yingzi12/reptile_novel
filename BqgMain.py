from bs4 import BeautifulSoup

from ParseHtml.DingdHtml import DingdHtml
from Util import LogUtil, HtmlUtil, HeadUtil
from lxml import etree

from entity.World import World

LogUtil.info("开始执行")
url="https://www.230book.net/xuanhuanxiaoshuo/1_2.html";


# responText=HtmlUtil.get_api_data(url,HeadUtil.bjg())
# if(responText == None):
#     LogUtil.error(f"url {url} 获取数据失败")
#
str='''
<!doctype html>
<html>
<head>
<title>玄幻小说_好看的玄幻小说_最新玄幻小说排行榜_顶点小说</title>
<meta http-equiv="Content-Type" content="text/html; charset=gbk" />
<meta name="keywords" content="玄幻小说,顶点小说,顶点小说网" />
<meta name="description" content="顶点小说致力于打造无广告无弹窗的在线玄幻小说阅读网站，提供玄幻小说在线阅读，网站没有弹窗广告页面简洁。" />
<meta name="applicable-device" content="pc" />
<link rel="stylesheet" type="text/css" href="/images/biquge.css"/>
<script type="text/javascript" src="https://libs.baidu.com/jquery/1.4.2/jquery.min.js"></script>
<script type="text/javascript" src="/images/bqg.js"></script>
</head>
<body>
	<div id="wrapper">
		<script>login();</script><script type="text/javascript" src="/images/yuedu.js"></script> 
		<div class="header">
			<div class="header_logo">
				<a href="https://www.230book.net">顶点小说</a>
			</div>
			<script>bqg_panel();</script>            
		</div>
		<div class="nav">
			<ul>
				<li><a href="/">首页</a></li>
                <li><a href="/modules/article/bookcase.php">我的书架</a></li>
				<li><a href="/xuanhuanxiaoshuo/">玄幻小说</a></li>
				<li><a href="/xiuzhenxiaoshuo/">修真小说</a></li>
				<li><a href="/dushixiaoshuo/">都市小说</a></li>
				<li><a href="/chuanyuexiaoshuo/">穿越小说</a></li>
				<li><a href="/wangyouxiaoshuo/">网游小说</a></li>
				<li><a href="/kehuanxiaoshuo/">科幻小说</a></li>
				<li><a href="/paihangbang/">排行榜单</a></li>
				<li><a href="/wanben/1_1">完本小说</a></li>
                <li><script type="text/javascript">yuedu();</script></li>
			</ul>
		</div>
        <div id="banner" style="display:none"></div>
		
        <div id="main">
        <div id="content">
<div id="hotcontent"><div class="ll">
      
       <div class="item">
        <div class="image"><a href="https://www.230book.net/book/503/"><img src="https://www.230book.net/files/article/image/0/503/503s.jpg" alt="诡秘之主"  width="120" height="150" /></a></div>
        <dl>
           <dt><span>爱潜水的乌贼</span><a href="https://www.230book.net/book/503/">诡秘之主</a></dt>
           <dd>    蒸汽与机械的浪潮中，谁能触及非凡？历史和黑暗的迷雾里，又是谁在耳语？我从诡秘中醒来，睁眼看见这个世界：
　　枪械，大炮，巨舰，飞空艇，差分机；魔药，占卜，诅咒，倒吊人...</dd>
        </dl>
        <div class="clear"></div>
      </div>
      
       <div class="item">
        <div class="image"><a href="https://www.230book.net/book/104/"><img src="https://www.230book.net/files/article/image/0/104/104s.jpg" alt="伏天氏"  width="120" height="150" /></a></div>
        <dl>
           <dt><span>净无痕</span><a href="https://www.230book.net/book/104/">伏天氏</a></dt>
           <dd>   东方神州，有人皇立道统，有圣贤宗门传道，有诸侯雄踞一方王国，诸强林立，神州动乱千万载，执此之时，一代天骄叶青帝及东凰大帝横空出世，斩人皇，驭圣贤，诸侯臣服，东方神州一统...</dd>
        </dl>
        <div class="clear"></div>
      </div>
      
       <div class="item">
        <div class="image"><a href="https://www.230book.net/book/2097/"><img src="https://www.230book.net/files/article/image/2/2097/2097s.jpg" alt="沧元图"  width="120" height="150" /></a></div>
        <dl>
           <dt><span>我吃西红柿</span><a href="https://www.230book.net/book/2097/">沧元图</a></dt>
           <dd>    我叫孟川，今年十五岁，是东宁府“镜湖道院”的当代大师兄。
...</dd>
        </dl>
        <div class="clear"></div>
      </div>
      
       <div class="item">
        <div class="image"><a href="https://www.230book.net/book/88/"><img src="https://www.230book.net/files/article/image/0/88/88s.jpg" alt="元尊"  width="120" height="150" /></a></div>
        <dl>
           <dt><span>天蚕土豆</span><a href="https://www.230book.net/book/88/">元尊</a></dt>
           <dd>    彼时的归途，已是一条命运倒悬的路。
    昔日的荣华，如白云苍狗，恐大梦一场。
    少年执笔，龙蛇飞动。
    是为一抹光芒劈开暮气沉沉之乱世，问鼎玉宇苍穹。
    复仇之路，...</dd>
        </dl>
        <div class="clear"></div>
      </div>
      
       <div class="item">
        <div class="image"><a href="https://www.230book.net/book/924/"><img src="https://www.230book.net/files/article/image/0/924/924s.jpg" alt="绝代名师"  width="120" height="150" /></a></div>
        <dl>
           <dt><span>相思洗红豆</span><a href="https://www.230book.net/book/924/">绝代名师</a></dt>
           <dd>   市二中的金牌老师孙默落水后，来到了中州唐国，成了一个刚毕业的实习老师，竟然有了一个白富美的未婚妻，未婚妻竟然还是一所名校的校长，不过这名校衰败了，即将摘牌除名，进行废校...</dd>
        </dl>
        <div class="clear"></div>
      </div>
      
       <div class="item">
        <div class="image"><a href="https://www.230book.net/book/5483/"><img src="https://www.230book.net/files/article/image/5/5483/5483s.jpg" alt="临渊行"  width="120" height="150" /></a></div>
        <dl>
           <dt><span>宅猪</span><a href="https://www.230book.net/book/5483/">临渊行</a></dt>
           <dd>    苏云怎么也没有想到，自己生活了十几年的天门镇，只有自己是人。他更没有想到天门镇外，方圆百里，是鼎鼎有名的无人区。临渊行。黑夜中临深渊而行，须得打起精神，如履薄冰！书友...</dd>
        </dl>
        <div class="clear"></div>
      </div>

     </div>
</div>

<div class="dahengfu"><script type="text/javascript">list1();</script></div>

<div id="newscontent">
<div class="l">
<h2>好看的玄幻小说最近更新列表</h2>
<ul>       

<li><span class="s2">《<a href="https://www.230book.net/book/46650/" target="_blank">修炼从简化功法开始</a>》</span><span class="s3"><a href="https://www.230book.net/book/46650/15371614.html" target="_blank">第七百章 望眼欲穿</a>(06-06)</span><span class="s5">努力吃鱼</span></li>
       
<li><span class="s2">《<a href="https://www.230book.net/book/49493/" target="_blank">大道圣主</a>》</span><span class="s3"><a href="https://www.230book.net/book/49493/15371422.html" target="_blank">第三百三十八章 战炼灵境！</a>(06-06)</span><span class="s5">唯幻</span></li>
       
<li><span class="s2">《<a href="https://www.230book.net/book/50573/" target="_blank">从肉体凡胎到粉碎星球</a>》</span><span class="s3"><a href="https://www.230book.net/book/50573/15370778.html" target="_blank">第二百三十三章 击溃</a>(06-05)</span><span class="s5">乘风御剑</span></li>
       
<li><span class="s2">《<a href="https://www.230book.net/book/23187/" target="_blank">吞噬星空之签到成神</a>》</span><span class="s3"><a href="https://www.230book.net/book/23187/15370483.html" target="_blank">第一千三百五十章吾即浑源，天命即定！</a>(06-05)</span><span class="s5">冥河老怪</span></li>
       
<li><span class="s2">《<a href="https://www.230book.net/book/50623/" target="_blank">太古龙神</a>》</span><span class="s3"><a href="https://www.230book.net/book/50623/15370460.html" target="_blank">第四十章 雷皇草</a>(06-05)</span><span class="s5">月如火</span></li>
       
<li><span class="s2">《<a href="https://www.230book.net/book/50618/" target="_blank">史上最强勇敢系统</a>》</span><span class="s3"><a href="https://www.230book.net/book/50618/15370455.html" target="_blank">第七百零五章 我只想对你不好，你却要杀我</a>(06-05)</span><span class="s5">淡定454</span></li>
       
<li><span class="s2">《<a href="https://www.230book.net/book/41445/" target="_blank">最后的黑暗之王</a>》</span><span class="s3"><a href="https://www.230book.net/book/41445/15369325.html" target="_blank">第576章 王之伟力</a>(06-05)</span><span class="s5">山川不念</span></li>
       
<li><span class="s2">《<a href="https://www.230book.net/book/47059/" target="_blank">奥术之主</a>》</span><span class="s3"><a href="https://www.230book.net/book/47059/15369162.html" target="_blank">第2548章 高级追求、家电下乡</a>(06-05)</span><span class="s5">姑苏献芹人</span></li>
       
<li><span class="s2">《<a href="https://www.230book.net/book/38145/" target="_blank">太上武神诀</a>》</span><span class="s3"><a href="https://www.230book.net/book/38145/15369025.html" target="_blank">第3544章 不见了</a>(06-05)</span><span class="s5">不是</span></li>
       
<li><span class="s2">《<a href="https://www.230book.net/book/41614/" target="_blank">我有一个破碎的游戏面板</a>》</span>
    <span class="s3"><a href="https://www.230book.net/book/41614/15368933.html" target="_blank">第五五二章 上眼药水，变相请功</a>(06-05)</span>
    <span class="s5">雨中鱼欲歌</span></li>
       
<li><span class="s2">《<a href="https://www.230book.net/book/40249/" target="_blank">悟性满级：剑阁观剑六十年</a>》</span><span class="s3"><a href="https://www.230book.net/book/40249/15368921.html" target="_blank">799、龙雀刀出，天地血祭！</a>(06-05)</span><span class="s5">我不是小号</span></li>
       
<li><span class="s2">《<a href="https://www.230book.net/book/11208/" target="_blank">凌天战尊</a>》</span><span class="s3"><a href="https://www.230book.net/book/11208/15368746.html" target="_blank">第4560章 青云圣宗，两大圣人齐出！</a>(06-05)</span><span class="s5">风轻扬</span></li>
       
<li><span class="s2">《<a href="https://www.230book.net/book/49367/" target="_blank">逆道斩神</a>》</span><span class="s3"><a href="https://www.230book.net/book/49367/15368732.html" target="_blank">第257章 巨人击鼓</a>(06-05)</span><span class="s5">闪电剑</span></li>
       
<li><span class="s2">《<a href="https://www.230book.net/book/32332/" target="_blank">战锤矮人</a>》</span><span class="s3"><a href="https://www.230book.net/book/32332/15368189.html" target="_blank">第四百三十六章 卡拉克金行</a>(06-05)</span><span class="s5">孝陵卫车神</span></li>
       
<li><span class="s2">《<a href="https://www.230book.net/book/50632/" target="_blank">系统降临开始无敌</a>》</span><span class="s3"><a href="https://www.230book.net/book/50632/15367802.html" target="_blank">第120章 挑战继续</a>(06-05)</span><span class="s5">破烂华哥</span></li>
       
<li><span class="s2">《<a href="https://www.230book.net/book/23693/" target="_blank">西游：人在天庭，朝九晚五</a>》</span><span class="s3"><a href="https://www.230book.net/book/23693/15367785.html" target="_blank">第1834章 弥勒佛面对众佛</a>(06-05)</span><span class="s5">雪山白术</span></li>

</ul>

<div class="page_b">
<table style=""><tr><td>
<div class="pagelink" id="pagelink"><em id="pagestats">2/244</em><a href="https://www.230book.net/xuanhuanxiaoshuo/1_1.html" class="first">1</a><a href="https://www.230book.net/xuanhuanxiaoshuo/1_1.html" class="pgroup">&lt;&lt;</a><a href="https://www.230book.net/xuanhuanxiaoshuo/1_1.html" class="prev">&lt;</a><a href="https://www.230book.net/xuanhuanxiaoshuo/1_1.html">1</a><strong>2</strong><a href="https://www.230book.net/xuanhuanxiaoshuo/1_3.html">3</a><a href="https://www.230book.net/xuanhuanxiaoshuo/1_4.html">4</a><a href="https://www.230book.net/xuanhuanxiaoshuo/1_5.html">5</a><a href="https://www.230book.net/xuanhuanxiaoshuo/1_6.html">6</a><a href="https://www.230book.net/xuanhuanxiaoshuo/1_7.html">7</a><a href="https://www.230book.net/xuanhuanxiaoshuo/1_8.html">8</a><a href="https://www.230book.net/xuanhuanxiaoshuo/1_9.html">9</a><a href="https://www.230book.net/xuanhuanxiaoshuo/1_10.html">10</a><a href="https://www.230book.net/xuanhuanxiaoshuo/1_3.html" class="next">&gt;</a><a href="https://www.230book.net/xuanhuanxiaoshuo/1_16.html" class="ngroup">&gt;&gt;</a><a href="https://www.230book.net/xuanhuanxiaoshuo/1_244.html" class="last">244</a><kbd><input name="page" type="text" size="4" maxlength="6" onkeydown="if(event.keyCode==13){window.location='https://www.230book.net/xuanhuanxiaoshuo/1_<{$page}>.html'.replace('<{$page|subdirectory}>', '/' + Math.floor(this.value / 1000)).replace('<{$page}>', this.value); return false;}" /></kbd><div style='clear:both'></div></div>
</td></tr></table>
</div>
</div>
<div class="r">
<h2>好看的玄幻小说</h2>
<ul>
<li><span class="s2"><a href="https://www.230book.net/book/5483/">临渊行</a></span><span class="s5">宅猪</span></li>
<li><span class="s2"><a href="https://www.230book.net/book/104/">伏天氏</a></span><span class="s5">净无痕</span></li>
<li><span class="s2"><a href="https://www.230book.net/book/2097/">沧元图</a></span><span class="s5">我吃西红柿</span></li>
<li><span class="s2"><a href="https://www.230book.net/book/6/">大道朝天</a></span><span class="s5">猫腻</span></li>
<li><span class="s2"><a href="https://www.230book.net/book/4048/">万古第一神</a></span><span class="s5">风青阳</span></li>
<li><span class="s2"><a href="https://www.230book.net/book/1/">时间掠夺</a></span><span class="s5">钦定</span></li>
<li><span class="s2"><a href="https://www.230book.net/book/5/">太监武帝</a></span><span class="s5">沉默的糕点</span></li>
<li><span class="s2"><a href="https://www.230book.net/book/14/">混在异界当医神</a></span><span class="s5">别听雨说</span></li>
<li><span class="s2"><a href="https://www.230book.net/book/41/">世尊</a></span><span class="s5">夜南听风</span></li>
<li><span class="s2"><a href="https://www.230book.net/book/28/">遮天神皇</a></span><span class="s5">夜云端</span></li>
<li><span class="s2"><a href="https://www.230book.net/book/29/">万古之王</a></span><span class="s5">快餐店</span></li>
<li><span class="s2"><a href="https://www.230book.net/book/65/">神能大风暴</a></span><span class="s5">夏炎炎</span></li>
<li><span class="s2"><a href="https://www.230book.net/book/34/">万古第一帝</a></span><span class="s5">天下青空</span></li>
<li><span class="s2"><a href="https://www.230book.net/book/48/">圣龙图腾</a></span><span class="s5">风青阳</span></li>
<li><span class="s2"><a href="https://www.230book.net/book/35/">人造人之传说战士</a></span><span class="s5">小半神</span></li>
<li><span class="s2"><a href="https://www.230book.net/book/36/">崛起诸天</a></span><span class="s5">冬日之阳</span></li>
<li><span class="s2"><a href="https://www.230book.net/book/47/">天行战记</a></span><span class="s5">七十二编</span></li>
<li><span class="s2"><a href="https://www.230book.net/book/64/">系统大逃杀</a></span><span class="s5">不言小佛</span></li>
<li><span class="s2"><a href="https://www.230book.net/book/49/">美食家在诸天</a></span><span class="s5">奥咏之弦</span></li>
<li><span class="s2"><a href="https://www.230book.net/book/81/">不可思议的奇幻之旅</a></span><span class="s5">海拉斯特黑袍</span></li>
<li><span class="s2"><a href="https://www.230book.net/book/79/">剑王朝‖争命</a></span><span class="s5">无罪</span></li>
<li><span class="s2"><a href="https://www.230book.net/book/73/">巫皇</a></span><span class="s5">傲天无痕</span></li>
<li><span class="s2"><a href="https://www.230book.net/book/85/">万界仙王</a></span><span class="s5">西门飘血</span></li>
<li><span class="s2"><a href="https://www.230book.net/book/87/">他从地狱来</a></span><span class="s5">纯洁滴小龙</span></li>
<li><span class="s2"><a href="https://www.230book.net/book/88/">元尊</a></span><span class="s5">天蚕土豆</span></li>
<li><span class="s2"><a href="https://www.230book.net/book/92/">天衣圣手</a></span><span class="s5">易语空</span></li>
<li><span class="s2"><a href="https://www.230book.net/book/98/">异界之超级大牧师</a></span><span class="s5">大个马铃薯</span></li>
<li><span class="s2"><a href="https://www.230book.net/book/100/">酋长别打脸</a></span><span class="s5">相思洗红豆</span></li>
<li><span class="s2"><a href="https://www.230book.net/book/106/">无限围城</a></span><span class="s5">东南秦氏</span></li>
<li><span class="s2"><a href="https://www.230book.net/book/108/">放逐之路：战争与守护</a></span><span class="s5">信邪的船</span></li>
 
</ul>
<div class="page_b page_b2">喜欢就收藏我们</div>
</div>
<div class="clear"></div></div>
</div>
</div>
        </div>

		</div>

		
        <div class="dahengfu"><script type="text/javascript">bottom();</script></div>
<div class="footer">
			<div class="footer_link"></div>
			<div class="footer_cont">
				<script>footer();right();dl();</script>
			</div>
		</div>
        
	</div>
</body>
<script charset="gbk" src="https://www.baidu.com/js/opensug.js"></script>
</html>
'''
# 使用Beautiful Soup解析HTML
soup = BeautifulSoup(str, 'html.parser')


# 提取id为"newscontent"的内容
newscontent_div = soup.find(id='newscontent')
# 找到class="l"下的ul元素
l_div = newscontent_div.find(class_='l')
ul = l_div.find('ul')

# 遍历所有的li元素
for li in ul.find_all('li'):
    # 提取详细信息
    title = li.find('span', class_='s2').text.strip().replace('《', '').replace('》', '')  # 提取标题
    book_link = li.find('a', href=True)['href']  # 提取书籍链接
    chapter_title = li.find('span', class_='s3').text.strip()  # 提取章节标题
    new_chapter = li.find('span', class_='s3').find('a').text.strip()  # 提取章节发布日期
    author = li.find('span', class_='s5').text.strip()  # 提取作者
    dingdHtml =  DingdHtml()
    dingdHtml.detail(book_link,title,author,"10","玄幻",new_chapter);
    # 打印详细信息
    # print("标题:", title)
    # print("书籍链接:", book_link)
    # print("章节标题:", chapter_title)
    # print("章节发布日期:", chapter_date)
    # print("作者:", author)
    # print()  # 用于分隔不同新闻
    # detailHtml=Detail(url);
    # detailHtml.bqg()