public class Print {
    public static void main(String[] args) {
        for (int i = 1; i <= 9; i++) {
            for (int j = 1; j <= i; j++) { // 关键：j <= i，而不是 j <= 10
                System.out.print(j + " * " + i + " = " + (i * j) + "\t");
            }
            System.out.println(); // 每行结束后换行
        }
    }
}