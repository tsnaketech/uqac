package stev.kwikemart;

public abstract class InvalidQuantityException extends ItemException {
   private static final long serialVersionUID = 1L;

   public InvalidQuantityException(String upc, String explanation) {
      super(upc, explanation);
   }

   public static final class InvalidQuantityForCategoryException extends InvalidQuantityException {
      private static final long serialVersionUID = 1L;

      public InvalidQuantityForCategoryException(String upc) {
         super(upc, "fractional quantities are not possible for this item category");
      }
   }
}
