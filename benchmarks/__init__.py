"""Benchmark registry.

To add a new category:
  1. Create  benchmarks/my_category.py
  2. Define  def my_category_benchmarks() -> list[Benchmark]: ...
  3. Add one line below:
       from .my_category import my_category_benchmarks
       Category.MY_CAT: my_category_benchmarks,
"""

from .models import Benchmark, Category, Connective, Constraint, Op, SZS, Verdict
from .single_axis import single_axis_benchmarks
from .box_2d import box_2d_benchmarks
from .box_3d import box_3d_benchmarks
from .composition import composition_benchmarks
from .cross_domain import cross_domain_benchmarks
from .policy_quality import policy_quality_benchmarks
from .boundary import boundary_benchmarks
from .logical_or import logical_or_benchmarks
from .logical_xone import logical_xone_benchmarks

CATEGORY_GENERATORS: dict[Category, callable] = {
    Category.SINGLE_AXIS:    single_axis_benchmarks,
    Category.BOX_2D:         box_2d_benchmarks,
    Category.BOX_3D:         box_3d_benchmarks,
    Category.COMPOSITION:    composition_benchmarks,
    Category.CROSS_DOMAIN:   cross_domain_benchmarks,
    Category.POLICY_QUALITY: policy_quality_benchmarks,
    Category.BOUNDARY:       boundary_benchmarks,
    Category.LOGICAL_OR:     logical_or_benchmarks,
    Category.LOGICAL_XONE:   logical_xone_benchmarks,
}

__all__ = [
    "CATEGORY_GENERATORS",
    "Benchmark", "Category", "Connective", "Constraint", "Op", "SZS", "Verdict",
]
