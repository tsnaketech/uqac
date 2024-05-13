package stev.kwikemart;

public abstract class CouponException extends ItemException {
   private static final long serialVersionUID = 1L;

   public CouponException(String upc, String message) {
      super(upc, message);
   }

   public static final class InvalidCouponQuantityException extends CouponException {
      private static final long serialVersionUID = 1L;

      public InvalidCouponQuantityException(String upc) {
         super(upc, "the quantity of a coupon must be 1");
      }
   }
}
