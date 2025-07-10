// Copyright 2025 The Lynx Authors. All rights reserved.
// Licensed under the Apache License Version 2.0 that can be found in the
// LICENSE file in the root directory of this source tree.

package com.lynx.tasm.performance.memory;

import java.util.Map;

/**
 * @brief Represents a memory record with a category, size in kilobytes, and detail information.
 */
public class MemoryRecord {
  /** The category of the memory record. like "image", "vm", "element" etc. */
  private String mCategory;
  /** The size of the memory record in kilobytes. */
  public float mSizeKb;
  /** The number of instances of the category. */
  public int mInstanceCount = 0;
  /** The detail information of the memory record. */
  public Map<String, String> mDetail = null;

  public MemoryRecord(
      String category, float sizeKb, int instanceCount, Map<String, String> detail) {
    mCategory = category;
    mSizeKb = sizeKb;
    mInstanceCount = instanceCount;
    mDetail = detail;
  }

  public String getCategory() {
    return mCategory;
  }
}
