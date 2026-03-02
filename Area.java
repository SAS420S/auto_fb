import java.util.Scanner;

class Area {
    Area(double base, double height) {
        double area = 0.5 * base * height;
        System.out.println("Area of Triangle = " + area);
    }
    Area(int length, int breadth) {
        int area = length * breadth;
        System.out.println("Area of Rectangle = " + area);
    }
    Area(double radius) {
        double area = Math.PI * radius * radius;
        System.out.println("Area of Circle = " + area);
    }
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        System.out.println("Select Shape:");
        System.out.println("1. Triangle");
        System.out.println("2. Rectangle");
        System.out.println("3. Circle");
        System.out.print("Enter your choice: ");
        int choice = sc.nextInt();
        switch (choice) {
            case 1:
                System.out.print("Enter base of triangle: ");
                double base = sc.nextDouble();
                System.out.print("Enter height of triangle: ");
                double height = sc.nextDouble();
                new Area(base, height);
                break;

            case 2:
                System.out.print("Enter length of rectangle: ");
                int length = sc.nextInt();
                System.out.print("Enter breadth of rectangle: ");
                int breadth = sc.nextInt();
                new Area(length, breadth);
                break;

            case 3:
                System.out.print("Enter radius of circle: ");
                double radius = sc.nextDouble();
                new Area(radius);
                break;

            default:
                System.out.println("Invalid Choice!");
        }
        sc.close();
    }
}
