# 混合制作镜头改版与工期成本核算

混合制作活动数据。时长为工时小时，结算为人民币元。镜头版本可部分复用，供应商补报的 original_entry 指向原费用。

## 资料格式

样例均为合成记录。CSV 使用 UTF-8，首行为列名。日期或时间采用 ISO 表示，多值字段以竖线分隔，空单元格表示该来源未记录。保留多版记录和部分未匹配的业务事实可供复查。

- shots.csv 的字段为 shot、project、variant、parent、segment_start、segment_end、method、final_state。
- deliveries.csv 的字段为 event、shot、variant、date、kind、review_until、hours。
- work_logs.csv 的字段为 log、shot、variant、block、date、activity、hours、cost。
- bookings.csv 的字段为 block、resource、start、stop、min_bill、projects、status。
- invoices.csv 的字段为 entry、block、booked、amount、state、original_entry。
- promises.csv 的字段为 project、deadline、requires、basis、committed。
- prerequisites.csv 的字段为 shot、variant、previous_shot、previous_variant、shared_resource。
- revisions.csv 的字段为 revision、project、shot、from_variant、to_variant、requested_on、start_second、end_second。

## 查验资料

使用 Python 3.11 及以上版本。资料检查只使用 Python 标准库。请在项目根目录运行。

~~~sh
python3 -m compileall -q tests
python3 -m unittest discover -s tests -v
~~~
