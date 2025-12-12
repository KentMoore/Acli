package filter;

import connect.HBaseConnect;
import org.apache.hadoop.hbase.CompareOperator;
import org.apache.hadoop.hbase.TableName;
import org.apache.hadoop.hbase.client.Connection;
import org.apache.hadoop.hbase.client.Result;
import org.apache.hadoop.hbase.client.Scan;
import org.apache.hadoop.hbase.client.Table;
import org.apache.hadoop.hbase.filter.BigDecimalComparator;
import org.apache.hadoop.hbase.filter.FilterList;
import org.apache.hadoop.hbase.filter.PageFilter;
import org.apache.hadoop.hbase.filter.SingleColumnValueFilter;
import org.apache.hadoop.hbase.util.Bytes;

import java.io.IOException;
import java.math.BigDecimal;

/**
 * 查看单价大于等于5块、小于等于20块的水果信息和销售信息
 * 分页显示，每页5条数据
 */
public class PriceRangePageFilter {
    static Connection connection;
    static Table table;

    public static void main(String[] args) throws IOException {
        connection = HBaseConnect.getConnection();
        TableName tableName = TableName.valueOf("commodity1:fruit_table");
        table = connection.getTable(tableName);

        // 过滤条件1：单价 >= 5
        SingleColumnValueFilter minPriceFilter = new SingleColumnValueFilter(
                Bytes.toBytes("sale_info"),
                Bytes.toBytes("unitPrice"),
                CompareOperator.GREATER_OR_EQUAL,
                new BigDecimalComparator(new BigDecimal("5")));

        // 过滤条件2：单价 <= 20
        SingleColumnValueFilter maxPriceFilter = new SingleColumnValueFilter(
                Bytes.toBytes("sale_info"),
                Bytes.toBytes("unitPrice"),
                CompareOperator.LESS_OR_EQUAL,
                new BigDecimalComparator(new BigDecimal("20")));

        // 分页过滤器：每页5条
        int pageSize = 5;
        PageFilter pageFilter = new PageFilter(pageSize);

        // 跟踪最新行的行键
        byte[] lastRowkey = null;
        int page = 1;

        System.out.println("========== 单价 >= 5 且 <= 20 的水果信息（分页显示，每页5条）==========");

        while (true) {
            System.out.println("----------------第" + page + "页-------------------");
            page++;

            // 创建Scan
            Scan scan = new Scan();

            // 组合价格过滤条件（AND条件）
            FilterList priceFilterList = new FilterList(
                    FilterList.Operator.MUST_PASS_ALL,
                    minPriceFilter,
                    maxPriceFilter);

            // 将价格过滤器和分页过滤器组合
            FilterList combinedFilterList = new FilterList(
                    FilterList.Operator.MUST_PASS_ALL,
                    priceFilterList,
                    pageFilter);

            scan.setFilter(combinedFilterList);

            if (lastRowkey != null) {
                scan.withStartRow(lastRowkey, false);
            }

            int count = 0;
            for (Result result : table.getScanner(scan)) {
                String rowkey = Bytes.toString(result.getRow());

                // 获取水果信息
                String fruitName = Bytes.toString(result.getValue(
                        Bytes.toBytes("fruit_info"), Bytes.toBytes("fruitName")));
                String fruitType = Bytes.toString(result.getValue(
                        Bytes.toBytes("fruit_info"), Bytes.toBytes("fruitType")));
                String fruitOrigin = Bytes.toString(result.getValue(
                        Bytes.toBytes("fruit_info"), Bytes.toBytes("fruitOrigin")));

                // 获取销售信息
                String unitPriceStr = Bytes.toString(result.getValue(
                        Bytes.toBytes("sale_info"), Bytes.toBytes("unitPrice")));
                BigDecimal unitPrice = new BigDecimal(unitPriceStr);

                Long quantity = Bytes.toLong(result.getValue(
                        Bytes.toBytes("sale_info"), Bytes.toBytes("quantity")));

                String totalPriceStr = Bytes.toString(result.getValue(
                        Bytes.toBytes("sale_info"), Bytes.toBytes("totalPrice")));
                BigDecimal totalPrice = new BigDecimal(totalPriceStr);

                System.out.println("水果编号:" + rowkey +
                        "，水果名:" + fruitName +
                        "，水果类型:" + fruitType +
                        "，水果产地:" + fruitOrigin +
                        "，单价：" + unitPrice +
                        "，销量：" + quantity +
                        "，销售额：" + totalPrice);

                count++;
                lastRowkey = result.getRow();
            }

            if (count < pageSize) {
                break;
            }
        }

        HBaseConnect.closeConnection();
    }
}
