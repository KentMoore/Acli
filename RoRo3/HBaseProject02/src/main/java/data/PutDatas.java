package data;

import com.csvreader.CsvReader;
import connect.HBaseConnect;
import org.apache.hadoop.hbase.TableName;
import org.apache.hadoop.hbase.client.Connection;
import org.apache.hadoop.hbase.client.Put;
import org.apache.hadoop.hbase.client.Table;
import org.apache.hadoop.hbase.util.Bytes;

import java.io.IOException;
import java.math.BigDecimal;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.List;

/**
 * 批量数据导入类
 * 
 * 优化点：
 * 1. Put 列表在循环外部创建，累积后批量提交
 * 2. 每 BATCH_SIZE 条数据提交一次，提高写入效率
 * 3. 使用 try-with-resources 确保资源自动关闭
 */
public class PutDatas {

    // 批量提交大小
    private static final int BATCH_SIZE = 1000;

    public static void main(String[] args) {
        // CSV 文件路径（建议改为配置文件或命令行参数）
        String path = "E:\\fruit_info.csv";

        // 获取连接
        Connection conn = HBaseConnect.getConnection();
        TableName tableName = TableName.valueOf("commodity1:fruit_table");

        // 使用 try-with-resources 自动关闭 Table
        try (Table table = conn.getTable(tableName)) {

            // 读取 CSV 数据
            List<String[]> csvData = readCsvByCsvReader(path);

            if (csvData.isEmpty()) {
                System.out.println("CSV 文件为空或读取失败");
                return;
            }

            // 在循环外部创建 Put 列表，累积后批量提交
            List<Put> puts = new ArrayList<>();
            int totalCount = 0;

            for (String[] row : csvData) {
                // 解析 CSV 数据
                String fruitNo = row[0];
                String fruitName = row[1];
                String fruitType = row[2];
                String fruitOrigin = row[3];
                BigDecimal unitPrice = new BigDecimal(row[4]);
                Long quantity = Long.valueOf(row[5]);
                BigDecimal totalPrice = new BigDecimal(row[6]);

                // 创建 Put 对象
                Put put = new Put(Bytes.toBytes(fruitNo));

                // fruit_info 列族
                put.addColumn(Bytes.toBytes("fruit_info"), Bytes.toBytes("fruitName"), Bytes.toBytes(fruitName));
                put.addColumn(Bytes.toBytes("fruit_info"), Bytes.toBytes("fruitType"), Bytes.toBytes(fruitType));
                put.addColumn(Bytes.toBytes("fruit_info"), Bytes.toBytes("fruitOrigin"), Bytes.toBytes(fruitOrigin));

                // sale_info 列族
                put.addColumn(Bytes.toBytes("sale_info"), Bytes.toBytes("unitPrice"), Bytes.toBytes(unitPrice));
                put.addColumn(Bytes.toBytes("sale_info"), Bytes.toBytes("quantity"), Bytes.toBytes(quantity));
                put.addColumn(Bytes.toBytes("sale_info"), Bytes.toBytes("totalPrice"), Bytes.toBytes(totalPrice));

                puts.add(put);

                // 每 BATCH_SIZE 条提交一次
                if (puts.size() >= BATCH_SIZE) {
                    table.put(puts);
                    totalCount += puts.size();
                    System.out.println("已提交 " + totalCount + " 条数据");
                    puts.clear();
                }
            }

            // 提交剩余数据
            if (!puts.isEmpty()) {
                table.put(puts);
                totalCount += puts.size();
            }

            System.out.println("数据导入完成，共导入 " + totalCount + " 条数据");

        } catch (IOException e) {
            System.err.println("数据导入失败: " + e.getMessage());
            e.printStackTrace();
        } finally {
            HBaseConnect.closeConnection();
        }
    }

    /**
     * 读取 CSV 文件
     * 
     * @param path CSV 文件路径
     * @return 数据列表
     */
    private static List<String[]> readCsvByCsvReader(String path) {
        List<String[]> arrList = new ArrayList<>();
        try {
            CsvReader csvReader = new CsvReader(path, ',', StandardCharsets.UTF_8);
            while (csvReader.readRecord()) {
                arrList.add(csvReader.getValues());
            }
            csvReader.close();
        } catch (Exception e) {
            System.err.println("读取 CSV 文件失败: " + e.getMessage());
            e.printStackTrace();
        }
        return arrList;
    }
}
